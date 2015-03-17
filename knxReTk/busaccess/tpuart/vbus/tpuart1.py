#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
    KONNEX/EIB-Protocol-Stack.

   (C) 2001-2014 by Christoph Schueler <cpu12.gems@googlemail.com>

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

import logging
import threading
import types

from kstack.busaccess.tpuart import utils
from kstack.busaccess.bif import BIF

"""
>>> FROM TPUART
===
MASK: 0x00
    ProductID.response ==> xxxxxxxx [0x00]
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
    DataEnd ==> 01xxxxxx [0x40]
    DataContinue ==> 10xxxxxx [0x80]
MASK: 0xf0
    PollingState ==> 1110xxxx [0xe0]
MASK: 0xf8
    AckInformation ==> 00010xxx [0x10]
MASK: 0xff
    Reset.request ==> 00000001 [0x01]
    State.request ==> 00000010 [0x02]
    ActivateBusmon ==> 00000101 [0x05]
    ProductID.request ==> 00100000 [0x20]
    ActivateBusyMode ==> 00100001 [0x21]
    ResetBusyMode ==> 00100010 [0x22]
    MxRstCnt ==> 00100100 [0x24]
    ActivateCRC ==> 00100101 [0x25]
    SetAddress ==> 00101000 [0x28]
    DataStart ==> 10000000 [0x80]
===
"""

##
## Services to TPUART1
##

SERVICES_TO_TPUART1 = (
    (0xc0,
        {
            0x40: 'DataEndReq',
            0x80: 'DataStartContinueReq',
        }
    ),
    (0xf0,
        {
            0xe0: 'PollingStateReq',
        }
    ),
    (0xf8,
        {
            0x10: 'AckInformationReq',
        }
    ),
    (0xff,
        {
            0x01: 'ResetReq',
            0x02: 'StateReq',
            0x05: 'ActivateBusmonReq',
            0x20: 'ProductIDReq',
            0x21: 'ActivateBusyModeReq',
            0x22: 'ResetBusyModeReq',
            0x24: 'MxRstCntReq',
            0x25: 'ActivateCRCReq',
            0x28: 'SetAddressReq',
        }
    )
)

##
##  U_State_Ind Error-Codes.
##

STATE_ERROR_SC = 0x80   # (slave collision)     - Collision is detected during transmission of polling state
STATE_ERROR_RE = 0x40   # (receive error)       - Corrupted bytes were sent by the host controller. Corruption involves
                        #                         incorrect parity (9-bit UART only) and stop bit of every byte as well
                        #                         as incorrect control octet, length or checksum of frame for transmission.
STATE_ERROR_TE = 0x20   # (transceiver error)   - Error detected during frame transmission (sending ‘0’ but receiving ‘1’).
STATE_ERROR_PE = 0x10   # (protocol error)      - An incorrect sequence of commands sent by the host controller is detected.
STATE_ERROR_TW = 0x08   # (thermal warning)     - Thermal warning condition is detected.

# cd \projekte\csProjects\k-ps\tools\kstack\busaccess\tpuart


REPETITION  = 0x20
L_DATA_CON  = 0x0b


##
## TODO: Library!!!
##

import functools

def synchronized(func):
    lock = threading.Lock()
    @functools.wraps(func)
    def decorated(*args, **kws):
        try:
            lock.acquire()
            result = func(*args, **kws)
        finally:
            lock.release()
        return result
    return decorated

@synchronized
def printHello(name):
    print "Hello, %s !!!" % name

#printHello("Chris")

class Service(object):

    def __init__(self, parent):
        self.idx = 0
        self.length = None
        self.parent = parent

    def setDefaultHandler(self):
        self.parent.setDefaultHandler()

    def reply(self, ch):
        self.parent.toHostBuffer.append(ch)

    def __call__(self, ch):
        raise NotImplementedError


class ResetReq(Service):

    def __call__(self, ch):
        print "resetReq"
        self.reply(0x00)
        self.reply(0x03)
        self.setDefaultHandler()


class StateReq(Service):

    def __call__(self, ch):
        print "stateReq"
        self.reply(0x07)
        self.setDefaultHandler()


class DataEndReq(Service):

    def __call__(self, ch):
        print "dataEndReq"


class DataStartContinueReq(Service):
    IDLE        = 0
    CONTINUE    = 1
    FINISHED    = 2

    def __init__(self, parent):
        super(DataStartContinueReq, self).__init__(parent)
        self.state = DataStartContinueReq.IDLE
        self.address = None
        self.datum = None
        self.finished = False
        self.checksum = 0xff
        self.length = None
        self.lengthByte = False
        self.lastIndex = None

    def __call__(self, ch):
        if self.state == DataStartContinueReq.IDLE:
            self.idx += 1
            self.setAddressOrDatum(self.idx, ch)
            if self.idx == 2:
                self.state = DataStartContinueReq.CONTINUE
                self.idx = 0
        elif self.state == DataStartContinueReq.CONTINUE:
            self.idx += 1
            self.setAddressOrDatum(self.idx, ch)

    def setAddressOrDatum(self, idx, ch):
        if idx % 2 == 0:
            self.datum = ch
            self.parent.txBuffer[self.address] = self.datum
            if self.lengthByte:
                self.lengthByte = False
                self.length = (ch & 0x0f) + 8 # TODO: OFFSET???
            if self.finished:
                self.state = DataStartContinueReq.FINISHED
                #print "Checksums", hex(ch), hex(self.checksum)
                self.parent.sendFrame(self.parent.txBuffer, self.length)
                self.setDefaultHandler()
            else:
                self.checksum ^= self.datum

        else:
            self.address = ch & 0x3f    # TODO: DON'T USE MagicNumbers!!!
            if (ch & 0xc0) == 0x40:
                self.finished = True
                self.lastIndex = ch & 0x3f
            elif self.address == 5:
                self.lengthByte = True

class Interface(BIF):

    def __init__(self, maxLSDUSize = 0x3f, **kws):
        super(Interface, self).__init__(**kws)
        self.masks, self.serviceMap = self.createServiceMap(SERVICES_TO_TPUART1)
        self.state = None
        self._closed = True
        self.busmonitorMode = False
        self.maxRstCount = 3
        self.toHostBuffer = []
        self.maxLSDUSize = maxLSDUSize
        self.initTxBuffer()
        self.configureLogger('tpuart1')
        self.setDefaultHandler()

    def configureLogger(self, name):
        logging.basicConfig(format = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s')
        #d = {'clientip': '192.168.0.1', 'user': 'fbloggs'}
        self.logger = logging.getLogger(name)
        #logger.warning('Protocol problem: %s', 'connection reset', extra=d)

    def setDefaultHandler(self):
        self.serviceHandler = self.dispatcher

    def initTxBuffer(self):
        self.txBuffer = [None] * self.maxLSDUSize

    @staticmethod
    def createServiceMap(services):
        masks = map(lambda x: x[0], services)
        serviceMap = {}
        for mask, serviceDict in services:
            serviceMap.setdefault(mask, {}).update(serviceDict)

        return masks, serviceMap

    def connect(self):
        """
        try:
            self.port.connect()
        except:
            raise
        else:
            self.connected = True
        """
        self._closed = False

    def disconnect(self):
        self._closed = True
        #self.port.close()

    def read(self, length):
        if self.toHostBuffer:
            #data =  self.toHostBuffer[-length : ]
            data =  self.toHostBuffer[ : length]
            data = filter(lambda x: x is not None, data)
            try:
                print "[read]", utils.hexDump(data)
            except:
                print "!? NULL ",
                for ch in data:
                    print ch,
            #del self.toHostBuffer[-length : ]
            del self.toHostBuffer[ : length]
            return data
        else:
            return None

    def write(self, request):
        print "[write]", utils.hexDump(request)
        for ch in request:
            self.serviceHandler(ch)

    def isAcknowledged(self):
        return False

    def repeat(self):
        pass

    #def checksum(self, frame):    # TODO: library!!!
    #    cs = 0xff
    #    for ch in frame:
    #        cs ^= ch
    #    return cs

    def sendFrame(self, frame, length):
        #length += 1
        print utils.hexDump(frame[ : length - 1])
        self.toHostBuffer.extend(frame[ : length])
        if not self.isAcknowledged():
            frame[0] &= (~REPETITION) & 0xff
            frame[length - 1] = checksum(frame[ : length - 1])
            for idx in range(self.maxRstCount):
                self.toHostBuffer.extend(frame[ : length])
                if self.isAcknowledged():
                    self.dataCon(True) # Positive Acknowledge
                    break
            self.dataCon(False)
        else:
            self.dataCon(True)    # Positive Acknowledge

    def dataCon(self, positive):
        conf = L_DATA_CON | (0x80 if positive else 0x00)
        self.toHostBuffer.append(conf)

    def dispatcher(self, service):
        #print "Service:", hex(service),
        for mask in self.masks:
            maskEntries = self.serviceMap[mask]
            maskedService = service & mask
            if maskedService in maskEntries.keys():
                self.serviceHandler = eval("%s(self)" % maskEntries[maskedService])
                result = self.serviceHandler(service)
                break

    @property
    def closed(self):
        return self._closed

    @closed.setter
    def closed(self, value):
        self._closed = value

"""
itf = Interface(hello = 'world')
itf.write([0x01, 0x02,
           0x80, 0xb0, 0x81, 0xaf, 0x82, 0xfe, 0x83, 0x11, 0x84, 0x52, 0x85, 0x60, 0x86, 0x80, 0x47, 0xbd]

#           0x80, 0xb0,
#           0x81, 0x11,     0x82, 0x52,
#           0x83, 0xaf,     0x84, 0xfe,
#           0x85, 0x60,     0x86, 0xc2,
#           0x46, 0xff]
    )
print itf.read(2)
print itf.read(1)
print itf.read(32)
print itf.read(32)
"""


"""

90  11  52  af fe  60  c2  df

90  11  52  af fe  63  43  40  00  20  3d
Quit
"""

# [write] 0x80, 0xb0, 0x81, 0xaf, 0x82, 0xfe, 0x83, 0x11, 0x84, 0x52, 0x85, 0x60, 0x86, 0x80, 0x47, 0xbd
