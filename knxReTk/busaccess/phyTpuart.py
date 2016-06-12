#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
   Konnex / EIB Reverserz Toolkit

   (C) 2001-2015 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

   This program is free software; you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

   s. FLOSS-EXCEPTION.txt
"""
__author__  = 'Christoph Schueler'
__version__ = '0.1.0'

from collections import namedtuple, OrderedDict
import Queue
import sys
import threading
import time
import types

from knxReTk.busaccess.tpuart import serialport
from knxReTk.utilz import helper
from knxReTk.busaccess.layer import Layer
from knxReTk.busaccess import knx
from knxReTk.utilz.threads import Thread
from knxReTk.busaccess.imi import IMI
from knxReTk.utilz.classes import SingletonBase
from knxReTk.busaccess.layer import MessageBuffer


BYTES_TO_READ = 32

RECEIVER_GROUP_0 = 0x07
RECEIVER_GROUP_1 = 0x7f
RECEIVER_GROUP_2 = 0xd3
RECEIVER_GROUP_3 = 0xff

RECEIVER = (
    (RECEIVER_GROUP_0, ),
    (RECEIVER_GROUP_1, ),
    (RECEIVER_GROUP_2, ),
    (RECEIVER_GROUP_3, ),
)

"""
>>> FROM TPUART
===
MASK: 0x00
    U_ProductID.response ==> xxxxxxxx [0x00]
MASK: 0x07
    State.response/indication ==> xxxxx111 [0x07]
MASK: 0x7f
    L_DATA.confirm ==> x0001011 [0x0b]
MASK: 0xd3
    L_EXT_DATA.req ==> 00x1xx00 [0x10]
    L_DATA.req ==> 10x1xx00 [0x90]
MASK: 0xff
    Reset-Indication ==> 00000011 [0x03]
    NotAcknowledge frame ==> 00001100 [0x0c]
    Busy frame ==> 11000000 [0xc0]
    Acknowledge frame ==> 11001100 [0xcc]
    L_POLLDATA.req ==> 11110000 [0xf0]
===


TO TPUART
===
MASK: 0xc0
    U_L_DataEnd_req ==> 01xxxxxx [0x40]
    U_L_DataCont_req ==> 10xxxxxx [0x80]
MASK: 0xf0
    U_PollingState_req ==> 1110xxxx [0xe0]
MASK: 0xf8
    U_AckInformation_req ==> 00010xxx [0x10]
MASK: 0xff
    U_Reset.request ==> 00000001 [0x01]
    U_State.request ==> 00000010 [0x02]
    U_ActivateBusmon_req ==> 00000101 [0x05]
    U_ProductID.request ==> 00100000 [0x20]
    U_ActivateBusyMode_req ==> 00100001 [0x21]
    U_ResetBusyMode_req ==> 00100010 [0x22]
    U_MxRstCnt_req ==> 00100100 [0x24]
    U_ActivateCRC_req ==> 00100101 [0x25]
    U_SetAddress_req ==> 00101000 [0x28]
    U_L_DataStart_req ==> 10000000 [0x80]
===
"""

##
## To TPUART.
##
U_L_DataEnd_req         = 0x40
U_L_DataCont_req        = 0x80
U_PollingState_req      = 0xe0
U_AckInformation_req    = 0x10

U_Reset_req             = 0x01
U_State_req             = 0x02
U_ActivateBusmon_req    = 0x05
U_ProductID_req         = 0x20
U_ActivateBusyMode_req  = 0x21
U_ResetBusyMode_req     = 0x22

U_MxRstCnt_req          = 0x24
U_ActivateCRC_req       = 0x25
U_SetAddress_req        = 0x28

U_L_DataStart_req       = 0x80


##
## From TPUART.
##

#MASK: 0x00
U_ProductID_res         = 0x00

#MASK: 0x07
U_State_ind             = 0x07

#MASK: 0x33
U_AckInformation_ind    = 0x00

#MASK: 0x7f
L_Data_con              = 0x0b

#MASK: 0xd3
L_Data_Extended_ind     = 0x10
L_Data_Standard_ind     = 0x90

#MASK: 0xff
U_Reset_ind             = 0x03

NAK                 = 0x0c
BUSY                = 0xc0
ACK                 = 0xcc


ACK_NACK            = 4
ACK_BUSY            = 2
ACK_ADDRESSED       = 1

L_Poll_Data_ind         = 0xf0


##
## Bus-Interface Variants.
##
VARIANT_TPUART_1    = 1
VARIANT_TPUART_2    = 2
VARIANT_NCN_5120    = 4

AVAILABLE_SERVICES = {
    # TO
    U_L_DataEnd_req         : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_L_DataCont_req        : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_PollingState_req      : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_AckInformation_req    : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_Reset_req             : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_State_req             : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_ActivateBusmon_req    : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_ProductID_req         : VARIANT_TPUART_2,
    U_ActivateBusyMode_req  : VARIANT_TPUART_2,
    U_ResetBusyMode_req     : VARIANT_TPUART_2,
    U_MxRstCnt_req          : VARIANT_TPUART_2,
    U_ActivateCRC_req       : VARIANT_TPUART_2,
    U_SetAddress_req        : VARIANT_TPUART_2,
    U_L_DataStart_req       : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,

    # FROM
    U_ProductID_res         : VARIANT_TPUART_2,
    U_State_ind             : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    L_Data_con              : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    L_Data_Extended_ind     : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    L_Data_Standard_ind     : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    U_Reset_ind             : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
    NAK                     : VARIANT_TPUART_1 | VARIANT_TPUART_2,
    BUSY                    : VARIANT_TPUART_1 | VARIANT_TPUART_2,
    ACK                     : VARIANT_TPUART_1 | VARIANT_TPUART_2,
    L_Poll_Data_ind         : VARIANT_TPUART_1 | VARIANT_TPUART_2 | VARIANT_NCN_5120,
}

SERVICE_NAMES = {
    # TO
    U_L_DataEnd_req         : "U_L_DataEnd_req",
    U_L_DataCont_req        : "U_L_DataCont_req",
    U_PollingState_req      : "U_PollingState_req",
    U_AckInformation_req    : "U_AckInformation_req",
    U_Reset_req             : "U_Reset_req",
    U_State_req             : "U_State_req",
    U_ActivateBusmon_req    : "U_ActivateBusmon_req",
    U_ProductID_req         : "U_ProductID_req",
    U_ActivateBusyMode_req  : "U_ActivateBusyMode_req",
    U_ResetBusyMode_req     : "U_ResetBusyMode_req",
    U_MxRstCnt_req          : "U_MxRstCnt_req",
    U_ActivateCRC_req       : "U_ActivateCRC_req",
    U_SetAddress_req        : "U_SetAddress_req",
    U_L_DataStart_req       : "U_L_DataStart_req",

    # FROM
    U_ProductID_res         : "U_ProductID_res",
    U_State_ind             : "U_State_ind",
    L_Data_con              : "L_Data_con",
    L_Data_Extended_ind     : "L_Data_Extended_ind",
    L_Data_Standard_ind     : "L_Data_Standard_ind",
    U_Reset_ind             : "U_Reset_ind",
    NAK                     : "NAK",
    BUSY                    : "BUSY",
    ACK                     : "ACK",
    L_Poll_Data_ind         : "L_Poll_Data_ind",
}

InternalService = namedtuple('InternalService', 'bytesExpected service mask')

INTERNAL_SERVICES = {
    U_Reset_req             : InternalService(1, U_Reset_ind,     0xff),
    U_State_req             : InternalService(1, U_State_ind,     0x07),
    U_ActivateBusmon_req    : InternalService(0, None,            None),
    U_ProductID_req         : InternalService(1, U_ProductID_res, 0x00),
    U_ActivateBusyMode_req  : InternalService(0, None,            None),
    U_ResetBusyMode_req     : InternalService(0, None,            None),
}


##
## Request Types.
##
REQUEST_TYPE_INTERNAL   = 0
REQUEST_TYPE_TRANSMIT   = 1


##
##  TPUART Status.
##

STATE_SLAVE_COLLISION        = 0x80
STATE_RECEIVE_ERROR          = 0x40
STATE_TRANSMIT_ERROR         = 0x20
STATE_PROTOCOL_ERROR         = 0x10
STATE_TEMPERATURE_WARNING    = 0x08

##
## Special Tokens.
##
CONTINUE            = -1

def makeComparator(mask, compareTo):
    def comparator(value):
        return (value & mask) == compareTo
    return comparator


class State(SingletonBase):

    def __str_(self):
        return "State[{0!s}]".format(self.__class__.__name__)

class Event(SingletonBase):

    def __str_(self):
        return "Event[{0!s}]".format(self.__class__.__name__)


##
## States.
##
IDLE                            = 0
AWAITING_RESPONSE_LOCAL         = 1
AWAITING_RESPONSE_TRANSMISSION  = 2
RECEIVING                       = 3
SENDING                         = 4


##
## Events.
##
REQUEST             = 0
INDICATION          = 1
TIMEOUT             = 2


class BusyException(Exception): pass

identity = lambda e: e

##
## only needed for bus-access, they get automatically downloaded and installed if you run setup.py.
##

Expectation = namedtuple('Expectation', 'service mask bytecount')


class BaseProcessor(object):

    def __init__(self, parent):
        self.parent = parent
        self.action = self.first
        self._done = False
        self.idx = 0

    @property
    def done(self):
        return self._done

    def first(self, octet):
        pass

    def consecutive(self, octet):
        pass

    def last(self, octet):
        pass

    def __call__(self, octet):
        self.action(octet)


class ConfirmedLocalCommand(BaseProcessor):

    def __init__(self, parent):
        super(ConfirmedLocalCommand, self).__init__(parent)
        self.frame = []

    def first(self, octet):
        if (octet & self.parent.expectation.mask) == self.parent.expectation.service:
            self.frame.append(octet)
            if self.parent.expectation.bytecount > 1:
                self.idx = 1
                self.action = self.consecutive
            else:
                self._done = True
                #print "We're done dude! ", octet
        else:
            pass

    def consecutive(self, octet):
        print "Cons: ", hex(octet),
        self.frame.append(octet)
        if self.idx < self.parent.expectation.bytecount:
            self.idx += 1
        else:
            self._done = True

REPETITION_MASK = 0xdf

class TransmissionCommand(BaseProcessor):

    def __init__(self, parent):
        super(TransmissionCommand, self).__init__(parent)
        self.frame = []
        self.bytecount = self.parent.expectation.bytecount
        self.repeated = False
        self.repetitionCounter = 0
        self.confirmation = False

    def last(self, octet):
        if octet & 0x7f == 0x0b:
            self.confirmation = (octet & 0x80) == 0x80

            mb = MessageBuffer(self.frame)
            mb.service = IMI.L_DATA_CON
            mb.confirmed = self.confirmation
            self.parent.dataLinkLayer.post(mb)

            self.parent.dataLinkLayer.release()
            #if self.confirmation:
            #    sys.exit()
            self._done = True
        else:
            #assert (octet & REPETITION_MASK) == (self.parent.sendBuffer[0] & REPETITION_MASK)
            if not ((octet & REPETITION_MASK) == (self.parent.sendBuffer[0] & REPETITION_MASK)):
                print "Uups [first]: '{0:02x}' != '{1:02x}'".format(octet, self.parent.sendBuffer[0] )
            self.idx = 1
            self.repetitionCounter += 1
            self.action = self.consecutive

    def statusString(self, octet):
        if (octet & 0xF8) == 0x00:
            return "OK"
        else:
            result = []
            if (octet & STATE_SLAVE_COLLISION) == STATE_SLAVE_COLLISION:
                result.append("SLAVE_COLLISION")
            elif (octet & STATE_RECEIVE_ERROR) == STATE_RECEIVE_ERROR:
                result.append("RECEIVE_ERROR")
            elif (octet & STATE_TRANSMIT_ERROR) == STATE_TRANSMIT_ERROR:
                result.append("TRANSMIT_ERROR")
            elif (octet & STATE_PROTOCOL_ERROR) == STATE_PROTOCOL_ERROR:
                result.append("PROTOCOL_ERROR")
            elif (octet & STATE_TEMPERATURE_WARNING) == STATE_TEMPERATURE_WARNING:
                result.append("TEMPERATURE_WARNING")
        return ' -  '.join(result)

    def first(self, octet):
        if (octet & 0x07) == 0x07:
            print "ERROR: ", hex(octet & 0xf8), self.statusString(octet)
            return
        else:
            #print "%02x %02x" % (octet, self.parent.sendBuffer[0])
            #assert octet & REPETITION_MASK == self.parent.sendBuffer[0] & REPETITION_MASK
            if not ((octet & REPETITION_MASK) == (self.parent.sendBuffer[0] & REPETITION_MASK)):
                print "Uups []first: '{0:02x}' != '{1:02x}'".format(octet, self.parent.sendBuffer[0] )
        self.repeated = not (octet & ~REPETITION_MASK == ~REPETITION_MASK)
        #if self.repeated:
        #    print "   *** Repeated!!"
        if (octet & self.parent.expectation.mask) == self.parent.expectation.service:
            self.frame.append(octet)
            if self.bytecount > 1:
                self.idx = 1
                self.action = self.consecutive
            else:
                self._done = True
        else:
            pass

    def consecutive(self, octet):
        self.frame.append(octet)
        self.idx += 1
        if self.idx == self.bytecount:
            self.action = self.last


class ReceiptionCommand(BaseProcessor):
    FRAME_FORMAT = {
        0b0010: "Standard-Frame",
        0b0000: "Long-Frame",
        0b0011: "Polling-Frame"
    }

    CLASSES = {
        0b0000: "system",
        0b0010: "alarm",
        0b0001: "high",
        0b0011: "low",
    }

    def __init__(self, parent):
        super(ReceiptionCommand, self).__init__(parent)
        self.frame = []
        self.previousFrame = []
        self.bytecount = self.parent.expectation.bytecount
        self.repeated = False
        self.repetitionCounter = 0
        self.confirmation = False

    def first(self, octet):
        self.frame.append(octet)
        frameFormat = (octet & 0xc0) >> 6
        rep = (octet & 0x20) >> 5
        klass = (octet & 0x0c) >> 2
        self.idx = 1
        self.action = self.consecutive
        #self.parent.port.write(0x11)
        #self.parent.ack(ACK_ADDRESSED)

    def consecutive(self, octet):
        self.frame.append(octet)
        if self.idx == 5:
            self.bytecount = (octet & 0x0f) + 2
        else:
            self.bytecount -= 1
            if self.bytecount == 1:
                self.action = self.last
        self.idx += 1

    def last(self, octet):
        self.frame.append(octet)
        mb = MessageBuffer(self.frame)
        mb.service = IMI.L_DATA_IND
        if self.frame[1 : -1] != self.previousFrame[1:-1]:   # TODO: check repeat! self.frame[0]
            # Don't post repeated frames.
            print "L_DATA_IND:", self.frame
            self.parent.dataLinkLayer.post(mb)
            self.previousFrame = self.frame
        else:
            print "CTRL:", hex(self.frame[0])
        self.frame = []
        self._done = True
        self.action = self.first


class NullProcessor(BaseProcessor): pass


class TPUARTServer(Thread):

    def __init__(self, port):
        super(TPUARTServer, self).__init__()
        self.expectation = Expectation(None, None, None)
        self.sendBuffer = None
        self.receiveBuffer = None
        self.port = port
        self._state = IDLE
        self.stateLock = threading.RLock()
        self.timer = None
        self.processor = NullProcessor(self)
        self.receiver = Receiver(port, self)
        self.receiver.start()

    def _getState(self):
        self.stateLock.acquire()
        state = self._state
        self.stateLock.release()
        return state

    def _setState(self, state):
        self.stateLock.acquire()
        self._state = state
        self.stateLock.release()

    state = property(_getState, _setState)

    def buisyWait(self):
        while self.state != IDLE:
            pass

    def serviceName(self, frame):
        if isinstance(frame, (list, tuple, )):
            serviceCode = frame[0]
        else:
            serviceCode = frame
        return SERVICE_NAMES.get(serviceCode)

    def execute(self):
        pass

    def indication(self, octet):
        assert isinstance(octet, types.IntType)
        self.processor(octet)
        # *** DEBUG
        #print "_IND: ", hex(octet)
        #print "%s 0x%02x %u" % (self.serviceName(self.expectation.service), self.expectation.mask, self.expectation.bytecount)
        # ***
        if self.state == AWAITING_RESPONSE_LOCAL:
            if self.processor.done:
                remaining = [] if len(self.processor.frame) == 1 else frame[1 : ]
                #print "Response-Frame: '%s{%s}'" % (self.serviceName(self.processor.frame[0]), remaining)
                self.state = IDLE
                self.processor = NullProcessor(self)
                self.timer.cancel()
        elif self.state == AWAITING_RESPONSE_TRANSMISSION:
            ## TODO: Error-Handling!!!
            if self.processor.done:
                self.timer.cancel()
                self.state = IDLE
                self.processor = NullProcessor(self)
                self.timer.cancel()
        elif self.state == IDLE:
            maskedOctet = octet & 0x0f
            if maskedOctet == U_State_ind:
                print "   *** U_State_Ind"
            maskedOctet = octet & 0xd3
            if maskedOctet == L_Data_Standard_ind:
                #print "   *** L_Data_Standard_ind"
                self.processor = ReceiptionCommand(self)
                self.processor(octet)
                self.state = RECEIVING
            elif maskedOctet == L_Data_Extended_ind:
                print "   *** L_Data_Extended_ind"
                self.processor = ReceiptionCommand(self)
                self.processor(octet)
                self.state = RECEIVING
            if octet == U_Reset_ind:
                print "   *** U_Reset_ind"
        elif self.state == RECEIVING:
            pass

    def expect(self, service, mask, byteCount):
        self.expectation = Expectation(service, mask, byteCount)

    def calculateTimeout(self, frame):
        if not isinstance(frame, (list, tuple, )):
            frame = [frame]
        return .25
        #return 0.05 + len(frame) *  0.05 # 0.005

    def command(self, frame, desiredState, receiverClass, wrappingFunc):
        if self.state != IDLE:
            return Exception("NOT IDLE.")
        self.state = SENDING
        self.sendBuffer = frame
        self.processor = receiverClass(self)
        frame = wrappingFunc(frame)

        #if isinstance(frame, (list, tuple)):
        #    print "WRITE-FRAME: ", helper.hexDump(frame)

        self.port.write(frame)
        self.timer = threading.Timer(self.calculateTimeout(frame), self.timeout, [self])
        self.timer.start()
        self.state = desiredState
        return True

    def internalCommand(self, frame, desiredState):
        return self.command(frame, desiredState, ConfirmedLocalCommand, identity)

    def requestTransmission(self, frame):
        frame.append(helper.checksum(frame))
        self.expect(0x00, 0x00, len(frame))
        return self.command(frame, AWAITING_RESPONSE_TRANSMISSION, TransmissionCommand, makeLDataRequest)

    def timeout(self, *args):
        print "*** TIMEOUT: "
        self.state = IDLE
        self.dataLinkLayer.release()
        self.timer.cancel()

    def internalCommandUnconfirmed(self, frame):
        print "internalCommandUnconfirmed: ", frame
        return self.internalCommand(frame, IDLE)

    def internalCommandConfirmed(self, frame):
        return self.internalCommand(frame, AWAITING_RESPONSE_LOCAL)

    ##
    ## Local Services.
    ##
    def activateBusmon(self):
        self.internalCommandUnconfirmed(U_ActivateBusmon_req)

    def activateBusyMode(self):
        self.internalCommandUnconfirmed(U_ActivateBusyMode_req)

    def resetBusyMode(self):
        self.internalCommandUnconfirmed(U_ResetBusyMode_req)

    def activateCRC(self):
        self.internalCommandUnconfirmed(U_ActivateCRC_req)

    def setRepetition(self, repetitions):
        self.internalCommandUnconfirmed([U_MxRstCnt_req, repetitions])

    def setAddress(self, address):
        self.internalCommandUnconfirmed([U_SetAddress_req, helper.wordToBytes(address)])

    def reset(self):
        self.expect(U_Reset_ind, 0xff, 1)
        self.internalCommandConfirmed(U_Reset_req)

    def ack(self, info):
        self.internalCommandUnconfirmed(U_AckInformation_req | (info & 0x07))

    def getState(self):
        self.expect(U_State_ind, 0xff, 1)
        self.internalCommandConfirmed(U_State_req)

    def getProductId(self):
        self.expect(U_ProductID_res, 0xff, 1)
        self.internalCommandConfirmed(U_ProductID_req)

    def getArbitrary(self, value):
        self.expect(0x00, 0x00, 1)
        self.internalCommandConfirmed(value)

    ##
    ##
    ##
    def connect(self, physAddr):
        frame = connectReq(physAddr)
        self.expect(0x00, 0x00, len(frame))
        #frame = makeLDataRequest(frame)
        #print "FRAME TO TRANSMIT: ", helper.hexDump(frame)
        self.requestTransmission(frame)


class Receiver(Thread):

    def __init__(self, port, parent):
        super(Receiver, self).__init__()
        self.port = port
        self.parent = parent

    def execute(self):
        data = self.port.read(BYTES_TO_READ)
        if data:
            for octet in data:
                #print "*** RCV: ", hex(octet)
                self.parent.indication(octet)
            #self.statemachine.indication(INDICATION, data)

def makeLDataRequest(frame):
    head = frame[0]
    tail = frame[1 : -1]
    fcs = frame[-1]
    request = []
    request.extend([U_L_DataStart_req, head])
    for idx, ch in enumerate(tail, 1):
        request.extend([U_L_DataCont_req | idx, ch])
    request.extend([U_L_DataEnd_req | (idx + 1), fcs])
    return request


def connectReq(physAddr):
    prolog = [0xBC, 0xAF, 0xFE]
    epilog = [0x60, 0x80]
    request = prolog + helper.wordToBytes(physAddr) + epilog
    fcs = helper.checksum(request)
    request.append(fcs)
    return request


class DataLinkLayer(Layer):

    sem = threading.Semaphore(value=1)

    def acquire(self):
        return DataLinkLayer.sem.acquire()

    def release(self):
        DataLinkLayer.sem.release()

    def l_Data_Req(self, message):
        self.server.buisyWait()
        self.acquire()
        frame = message.asStandardFrame()
        frame.frameType = knx.FRAME_STANDARD
        self.server.requestTransmission(message.asList())

    def l_PollData_Req(self, message):
        print "l_PollData_Req"

    SERVICES = {
        IMI.L_DATA_REQ: l_Data_Req,
        IMI.L_POLL_DATA_REQ: l_PollData_Req,
    }

    SERVICE_GROUP = IMI.LL_SERVICES

