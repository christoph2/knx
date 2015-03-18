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


import threading

from knxReTk.busaccess import knx
from knxReTk.busaccess.layer import Layer, MessageBuffer
from knxReTk.busaccess.imi import IMI
from knxReTk.utilz.classes import SingletonBase

MAX_REPETITION_COUNT    = 3
CONNECTION_TIMEOUT      = 6.0
ACKNOWLEDGE_TIMEOUT     = 3.0

##
##  TPCI-Codings.
##
TPCI_UDT                = 0x00  # Unnumbered Data.
TPCI_NDT                = 0x40  # Numbered Data (T_DATA_CONNECTED_REQ_PDU).
TPCI_UCD                = 0x80  # Unnumbered Control.
TPCI_NCD                = 0xC0  # Numbered Control (TACK/TNACK).

TPCI_ACK_PDU            = 0xC2
TPCI_NAK_PDU            = 0xC3

TPCI_CONNECT_REQ_PDU    = 0x80
TPCI_DISCONNECT_REQ_PDU = 0x81

TPCI_DATA_TAG_GROUP_PDU = 0x04  # Interface-Objects using Group-Addressing (LTE-HEE).


##
## StateMachine
##
class EventType(SingletonBase):
    EVENT_CONNECT_IND           = 0
    EVENT_DISCONNECT_IND        = 1
    EVENT_DATA_CONNECTED_IND    = 2
    EVENT_ACK_IND               = 3
    EVENT_NAK_IND               = 4
    EVENT_CONNECT_REQ           = 5
    EVENT_DISCONNECT_REQ        = 6
    EVENT_DATA_CONNECTED_REQ    = 7
    EVENT_CONNECT_CON           = 8
    EVENT_DISCONNECT_CON        = 9
    EVENT_DATA_CONNECTED_CON    = 10
    EVENT_ACK_CON               = 11
    EVENT_NAK_CON               = 12
    EVENT_TIMEOUT_CON           = 13
    EVENT_TIMEOUT_ACK           = 14
    EVENT_UNDEFINED             = 15

    _Names = {
        EVENT_CONNECT_IND:          "EVENT_CONNECT_IND",
        EVENT_DISCONNECT_IND:       "EVENT_DISCONNECT_IND",
        EVENT_DATA_CONNECTED_IND:   "EVENT_DATA_CONNECTED_IND",
        EVENT_ACK_IND:              "EVENT_ACK_IND",
        EVENT_NAK_IND:              "EVENT_NAK_IND",
        EVENT_CONNECT_REQ:          "EVENT_CONNECT_REQ",
        EVENT_DISCONNECT_REQ:       "EVENT_DISCONNECT_REQ",
        EVENT_DATA_CONNECTED_REQ:   "EVENT_DATA_CONNECTED_REQ",
        EVENT_CONNECT_CON:          "EVENT_CONNECT_CON",
        EVENT_DISCONNECT_CON:       "EVENT_DISCONNECT_CON",
        EVENT_DATA_CONNECTED_CON:   "EVENT_DATA_CONNECTED_CON",
        EVENT_ACK_CON:              "EVENT_ACK_CON",
        EVENT_NAK_CON:              "EVENT_NAK_CON",
        EVENT_TIMEOUT_CON:          "EVENT_TIMEOUT_CON",
        EVENT_TIMEOUT_ACK:          "EVENT_TIMEOUT_ACK",
        EVENT_UNDEFINED:            "EVENT_UNDEFINED"
    }

    @classmethod
    def toString(klass, value):
        return klass._Names.get(value, "<INAVLID EVENT>")


class StateType(SingletonBase):
    STATE_CLOSED                = 0
    STATE_OPEN_IDLE             = 1
    STATE_OPEN_WAIT             = 2
    STATE_CONNECTING            = 3

    _Names = {
        STATE_CLOSED:     "STATE_CLOSED",
        STATE_OPEN_IDLE:  "STATE_OPEN_IDLE",
        STATE_OPEN_WAIT:  "STATE_OPEN_WAIT",
        STATE_CONNECTING: "STATE_CONNECTING",
    }

    @classmethod
    def toString(klass, value):
        return klass._Names.get(value, "<INAVLID STATE>")


class StateMachine(SingletonBase):

    def __init__(self):
        self._state = StateType.STATE_CLOSED
        self._sequenceNumberSend = 0
        self._sequenceNumberReceived = 0
        self._repetitionCount = 0
        self._sequenceNumberOfPDU = 0
        self._sourceAddress = 0
        self._connectionAddress = 0
        self._storedMessage = None
        self._connectionTimer = None
        self._acknowledgeTimer = None

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def sequenceNumberSend(self):
        return (self._sequenceNumberSend & 0x0f)

    @sequenceNumberSend.setter
    def sequenceNumberSend(self, value):
        self._sequenceNumberSend = (value & 0x0f)

    @property
    def sequenceNumberReceived(self):
        return (self._sequenceNumberReceived & 0x0f)

    @sequenceNumberReceived.setter
    def sequenceNumberReceived(self, value):
        self._sequenceNumberReceived = (value & 0x0f)

    @property
    def repetitionCount(self):
        return self._repetitionCount

    @repetitionCount.setter
    def repetitionCount(self, value):
        self._repetitionCount = value

    @property
    def sequenceNumberOfPDU(self):
        return (self._sequenceNumberOfPDU & 0x0f)

    @sequenceNumberOfPDU.setter
    def sequenceNumberOfPDU(self, value):
        self._sequenceNumberOfPDU = (value & 0x0f)

    @property
    def sourceAddress(self):
        return self._sourceAddress

    @sourceAddress.setter
    def sourceAddress(self, value):
        self._sourceAddress = value

    @property
    def connectionAddress(self):
        return self._connectionAddress

    def storeMessage(self, message):
        self._storedMessage = message

    def restoreMessage(self):
        return self._storedMessage

    @connectionAddress.setter
    def connectionAddress(self, value):
        self._connectionAddress = value

    def startConnectionTimeoutTimer(self):
        self._connectionTimer = threading.Timer(CONNECTION_TIMEOUT, self.connectionTimeoutHandler)

    def stopConnectionTimeoutTimer(self):
        if self._connectionTimer:
            self._connectionTimer.cancel()

    def restartConnectionTimeoutTimer(self):
        self.startConnectionTimeoutTimer()
        self.startConnectionTimeoutTimer()

    def connectionTimeoutHandler(self):
        print "*** connectionTimeoutHandler"
        self.stopConnectionTimeoutTimer()
        self(EventType.EVENT_TIMEOUT_CON)

    def startAcknowledgeTimeoutTimer(self):
        self._acknowledgeTimer = threading.Timer(ACKNOWLEDGE_TIMEOUT, self.acknowledgeTimeoutHandler)

    def stopAcknowledgeTimeoutTimer(self):
        if self._acknowledgeTimer:
            self._acknowledgeTimer.cancel()

    def restartAcknowledgeTimeoutTimer(self):
        self.stopAcknowledgeTimeoutTimer()
        self.startAcknowledgeTimeoutTimer()

    def acknowledgeTimeoutHandler(self):
        print "*** acknowledgeTimeoutHandler"
        self.stopAcknowledgeTimeoutTimer()

    def __call__(self, event):
        print "State: %s - Event: %s" % (StateType.toString(self._state), EventType.toString(event), ),

        #
        eventHandler = self.EVENT_HANDLER[event]
        entry = StateMachine.STATE_TABLE[eventHandler(self)]
        action, nextState = entry[self.state]
        print "NextState: ", nextState
        self.state = nextState
        action(self)

        #void KnxTlc_StateMachine(KNX_TlcEventType event)
        #    KnxTlc_ActionType action;
        #
        #    printf("STATE: %u EVENT: %u ", KnxTlc_GetState(), event);
        #
        #    action = KnxTlc_Actions[((event < KNX_TLC_EVENT_UNDEFINED) ? TLC_Events[event]() : KnxTlc_Event_Undefined())].Action[KnxTlc_GetState()];
        #    KnxTlc_SetState(action.Next);
        #    printf("NEXT-STATE: %u\n", action.Next);
        #    action.Function();

    def A0(self):
        # Do nothing.
        print "A0"
        pass

    def A1(self):
        print "A1"
        self.connectionAddress = message.asStandardFrame().source
        self.message.service = IMI.T_CONNECT_IND
        self.layer.post(self.message)
        self.sequenceNumberSend = 0
        self.sequenceNumberReceived = 0
        self.startConnectionTimeoutTimer()

    def A2(self):
        print "A2"
        self.parent.t_Ack_Req(self.sourceAddress, self.connectionAddress, self.sequenceNumberReceived)
        self.sequenceNumberReceived = self.sequenceNumberReceived + 1
        self.restartConnectionTimeoutTimer()

    def A3(self):
        print "A3"
        self.parent.t_Ack_Req(self.sourceAddress, self.connectionAddress, self.sequenceNumberReceived)
        self.restartConnectionTimeoutTimer()

    def A4(self):
        print "A4"
        self.parent.t_Nak_Req(self.sourceAddress, self.connectionAddress, self.sequenceNumberReceived)
        self.restartConnectionTimeoutTimer()

    def A5(self):
        print "A5"
        # Send a T_Disconnect.ind to the user.
        # Handled by callback.
        # T_Disconnect_Ind(KnxMsg_ScratchBufferPtr, KnxTlc_GetConnectionAddress(), KnxTlc_GetSourceAddress(), /*KnxADR_GetPhysAddr() */);
        self.stopAcknowledgeTimeoutTimer()
        self.stopConnectionTimeoutTimer()

    def A6(self):
        print "A6"
        ##
        ##  Send a N_Data_Individual.req with T_DISCONNECT_REQ_PDU, priority = SYSTEM,
        ##  destination = connection_address, sequence = 0 to the network layer (remote device).
        ##
        self.parent.n_Disconnect_Req(self.sourceAddress, self.connectionAddress)
        #  Send a T_Disconnect.ind to the user.
        #  Handled by callback.
        self.stopAcknowledgeTimeoutTimer()
        self.stopConnectionTimeoutTimer()

    def A7(self):
        print "A7"
        ##
        ##  Store the received T_Data_Connected.req and send as a N_Data_Individual.req
        ##  with T_DATA_CONNECTED_REQ_PDU,destination = connection_address,
        ##  sequence = SeqNoSend to the network layer (remote device).
        ##
        self.storeMessage(self.message.copy())
        frame = self.message.asStandardFrame()
        frame.seqNo = self.sequenceNumberSend
        frame.dest = self.connectionAddress
        self.message.service = N_DATA_INDIVIDUAL_REQ    # T_DATA_CONNECTED_REQ
        self.parent.post(self.message)
        self.repetitionCount = 0
        self.startAcknowledgeTimeoutTimer()
        self.restartConnectionTimeoutTimer()

    def A8(self):
        print "A8"
        self.startAcknowledgeTimeoutTimer()
        self.sequenceNumberSend += 1

        message = self.restoreMessage()
        ##  Send the stored buffer as a T_Data_Connected.con with cleared errorbits,
        ##  connection number = 0 to the user.
        ##  dest: connection_addr, sequence=SeqNoSend.
        self.restartConnectionTimeoutTimer()

    def A8a(self):
        print "A8a"
        self.stopAcknowledgeTimeoutTimer()
        self.sequenceNumberSend += 1
        self.restartConnectionTimeoutTimer()

    def A9(self):
        print "A9"
        #  Send the stored message as a N_Data_Individual.req to the network layer (remote device).
        message = self.restoreMessage()
        message.asStandardFrame().seqNo = self.sequenceNumberSend
        message.service = IMI.N_DATA_INDIVIDUAL_REQ
        self.parent.post(message)
        self.repetitionCount += 1
        self.startAcknowledgeTimeoutTimer()
        self.restartConnectionTimeoutTimer()

    def A10(self):
        print "A10"
        #  Send a N_Data_Individual.req with T_DISCONNECT_REQ_PDU Priority = SYSTEM, */
        #  Destination = source (rbuffer), Sequence = 0 back to sender. */

        frame = self.message.asStandardFrame()
        print "t_Disconnect_Req from: %04x to: %04x" % (frame.dest, frame.source, )
        self.parent.t_Disconnect_Req(frame.dest, frame.source)

    def A11(self):
        print "A11"
        #  Store event back and handle after next event. Don't change order of T_Data_Connected.req events.

    def A12(self):
        print "A12"
        #  send N_Data_Individual.req with T_CONNECT_REQ_PDU
        self.sequenceNumberSend = 0
        self.sequenceNumberReceived = 0
        self.startConnectionTimeoutTimer()

    def A13(self):
        print "A13"
        #  Send a T_Connect.con to the user.

    def A14(self):
        print "A14"
        #  Send a N_Data_Individual.req with T_DISCONNECT_REQ_PDU, priority = SYSTEM, */
        #  destination = connection_address, sequence = 0 to the network layer (remote device). */
        #  Send a T_Disconnect.con to the user. */
        self.stopAcknowledgeTimeoutTimer()
        self.stopConnectionTimeoutTimer()

    def A14b(self):
        print "A14b"
        #  Send a N_Data_Individual.req with T_DISCONNECT_REQ_PDU, priority = SYSTEM, */
        #  destination = connection_address, sequence = 0 to the network layer (remote device). *
        self.stopAcknowledgeTimeoutTimer()
        self.stopConnectionTimeoutTimer()

    def A15(self):
        print "A15"
        #  Send a T_Disconnect.con to the management user.
        self.stopAcknowledgeTimeoutTimer()
        self.stopConnectionTimeoutTimer()


    STATE_TABLE = (
        ( (A1, StateType.STATE_OPEN_IDLE),  (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
        ( (A1, StateType.STATE_OPEN_IDLE),  (A10, StateType.STATE_OPEN_IDLE),   (A10, StateType.STATE_OPEN_WAIT),   (A10, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A5, StateType.STATE_CLOSED),       (A5, StateType.STATE_CLOSED),       (A5, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A2, StateType.STATE_OPEN_IDLE),    (A2, StateType.STATE_OPEN_WAIT),    (A6, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A3, StateType.STATE_OPEN_IDLE),    (A3, StateType.STATE_OPEN_WAIT),    (A3, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A4, StateType.STATE_OPEN_IDLE),    (A4, StateType.STATE_OPEN_WAIT),    (A6, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A10, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A8, StateType.STATE_OPEN_IDLE),    (A6, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A6, StateType.STATE_CLOSED),       (A6, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A10, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A6, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A6, StateType.STATE_CLOSED),       (A9, StateType.STATE_OPEN_WAIT),    (A6, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A6, StateType.STATE_CLOSED),       (A6, StateType.STATE_CLOSED),       (A6, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A10, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A7, StateType.STATE_OPEN_WAIT),    (A11, StateType.STATE_OPEN_WAIT),   (A11, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A6, StateType.STATE_CLOSED),       (A6, StateType.STATE_CLOSED),       (A6, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A9, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A6, StateType.STATE_CLOSED),       (A0, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A13, StateType.STATE_OPEN_IDLE), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A5, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
        ( (A12, StateType.STATE_CONNECTING), (A6, StateType.STATE_CLOSED),      (A6, StateType.STATE_CLOSED),       (A6, StateType.STATE_CLOSED), ),
        ( (A15, StateType.STATE_CLOSED),    (A14, StateType.STATE_CLOSED),      (A14, StateType.STATE_CLOSED),      (A14, StateType.STATE_CLOSED), ),
        ( (A0, StateType.STATE_CLOSED),     (A0, StateType.STATE_OPEN_IDLE),    (A0, StateType.STATE_OPEN_WAIT),    (A0, StateType.STATE_CONNECTING), ),
    )


    def Event_Connect_Ind(self):
        if self.sourceAddress == self.connectionAddress:
            return 0
        else:
            return 1

    def Event_Disconnect_Ind(self):
        if self.sourceAddress == self.connectionAddress:
            return 2
        else:
            return 3

    def Event_DataConnected_Ind(self):
        if self.sourceAddress == self.connectionAddress:
            if self.sequenceNumberOfPDU == self.sequenceNumberReceived:
                eventNum = 4
            elif self.sequenceNumberOfPDU == (self.sequenceNumberReceived -1):
                eventNum = 5
            elif self.sequenceNumberOfPDU != (self.sequenceNumberReceived -1):
                eventNum = 6
            else:
                eventNum = 27
        else:
            eventNum = 7
        return eventNum

    def Event_Ack_Ind(self):
        if self.sourceAddress == self.connectionAddress:
            print "OK, sourceAddr == connectionAddr."
            if self.sequenceNumberOfPDU == self.sequenceNumberSend:
                eventNum = 8
                print "OK, seqNoPDU == seqNoSend."
            else:
                eventNum = 9
                print "NOT-OK, seqNoPDU != seqNoSend!"
        else:
            eventNum = 10
            print "NOT-OK, sourceAddr != connectionAddr!"
            print "<<%04X>><<%04X>>" % (self.sourceAddress, self.connectionAddress, )
        return eventNum

    def Event_Nak_Ind(self):
        if self.sourceAddress == self.connectionAddress:
            if self.sequenceNumberOfPDU != self.sequenceNumberSend:
                eventNum = 11
            else:
                if self.repetitionCount < MAX_REPETITION_COUNT:
                    eventNum = 12
                else:
                    eventNum = 13
        else:
            eventNum = 14
        return eventNum

    def Event_Connect_Req(self):
        return 25

    def Event_Disconnect_Req(self):
        return 26

    def Event_DataConnected_Req(self):
        return 15

    def Event_Connect_Con(self):
        print("Event_ConnectCon: ", self.message.confirmed)
        if self.message.confirmed:
            return 19
        else:
            return 20

    def Event_Disconnect_Con(self):
        return 21

    def Event_DataConnected_Con(self):
        return 22

    def Event_Ack_Con(self):
        return 23

    def Event_Nak_Con(self):
        return 24

    def Event_Timeout_Con(self):
        return 16

    def Event_Timeout_Ack(self):
        if self.repetitionCount < MAX_REPETITION_COUNT:
            return 17
        else:
            return 18

    def Event_Undefined(self):
        return 27

    EVENT_HANDLER = (
        Event_Connect_Ind,
        Event_Disconnect_Ind,
        Event_DataConnected_Ind,
        Event_Ack_Ind,
        Event_Nak_Ind,
        Event_Connect_Req,
        Event_Disconnect_Req,
        Event_DataConnected_Req,
        Event_Connect_Con,
        Event_Disconnect_Con,
        Event_DataConnected_Con,
        Event_Ack_Con,
        Event_Nak_Con,
        Event_Timeout_Con,
        Event_Timeout_Ack,
        Event_Undefined
    )


class TransportLayerConnected(Layer):

    def __init__(self):
        super(TransportLayerConnected, self).__init__()
        self.stateMachine = StateMachine()
        self.stateMachine.layer = self

    def n_DataIndividual_Ind(self, message):
        print "TransportLayerConnected: n_DataIndividual_Ind"
        frame = message.asStandardFrame()
        tpci = frame.tpci
        tpciMasked = (frame.tpci & 0xc0)
        if tpciMasked == TPCI_UDT:      # Unnumbered Data (1:1-Connection-Less).
            message.service = IMI.T_DATA_INDIVIDUAL_IND
            self.post(message)
        elif tpciMasked == TPCI_NDT:    # Numbered Data (T_DATA_CONNECTED_REQ_PDU, 1:1-Connection-Oriented).
            self.sequenceNumberOfPDU = frame.seqNo
            #KnxTlc_StateMachine(KNX_TLC_EVENT_DATA_CONNECTED_IND);
            frame.service = IMI.T_DATA_CONNECTED_IND
            self.post(message)
        elif tpciMasked == TPCI_UCD:    # Unnumbered Control. (CONNECT|DISCONNECT).
            print "    CONN/DIS!: 0x%02x" % frame.tpci
            if tpci == TPCI_CONNECT_REQ_PDU:        # T_CONNECT_IND.
                #KnxTlc_StateMachine(KNX_TLC_EVENT_CONNECT_IND)
                pass
            elif tpci == TPCI_DISCONNECT_REQ_PDU:   # T_DISCONNECT_IND.
                #KnxTlc_StateMachine(KNX_TLC_EVENT_DISCONNECT_IND)
                pass
            else:
                assert False
        elif tpciMasked == TPCI_NCD:    # umbered Control (ACK| NAK).
            tpci &= 0xC3
            self.sequenceNumberOfPDU = frame.seqNo
            if tpci == TPCI_ACK_PDU:
                # KnxTlc_StateMachine(KNX_TLC_EVENT_ACK_IND);
                pass
            elif tpci == TPCI_NAK_PDU:
                # KnxTlc_StateMachine(KNX_TLC_EVENT_NAK_IND)
                pass
            else:
                assert False
        else:
            assert False

    def n_DataIndividual_Con(self, message):
        #print "TransportLayerConnected: n_DataIndividual_Con"
        frame = message.asStandardFrame()
        self.stateMachine.message = message
        tpci = frame.tpci
        tpciMasked = (frame.tpci & 0xc0)
        if tpciMasked == TPCI_UDT:      # Unnumbered Data (1:1-Connection-Less).
            message.service = IMI.T_DATA_INDIVIDUAL_CON
            self.post(message)
        elif tpciMasked == TPCI_NDT:    # Numbered Data (T_DATA_CONNECTED_REQ_PDU, 1:1-Connection-Oriented).
            #KnxTlc_StateMachine(KNX_TLC_EVENT_DATA_CONNECTED_CON);
            self.stateMachine(EventType.EVENT_DATA_CONNECTED_CON)
        elif tpciMasked == TPCI_UCD:    # Unnumbered Control. (CONNECT|DISCONNECT).
            print "    CONN/DIS!: 0x%02x" % frame.tpci
            if tpci == TPCI_CONNECT_REQ_PDU:        # T_CONNECT_CON.
                #KnxTlc_StateMachine(KNX_TLC_EVENT_CONNECT_CON)
                self.stateMachine(EventType.EVENT_CONNECT_CON)
            elif tpci == TPCI_DISCONNECT_REQ_PDU:   # T_DISCONNECT_IND.
                #KnxTlc_StateMachine(KNX_TLC_EVENT_DISCONNECT_CON)
                self.stateMachine(EventType.EVENT_DISCONNECT_CON)
            else:
                assert False
        elif tpciMasked == TPCI_NCD:    # umbered Control (ACK| NAK).
            tpci &= 0xC3
            if tpci == TPCI_ACK_PDU:
                # KnxTlc_StateMachine(KNX_TLC_EVENT_ACK_CON);
                self.stateMachine(EventType.EVENT_ACK_CON)
            elif tpci == TPCI_NAK_PDU:
                # KnxTlc_StateMachine(KNX_TLC_EVENT_NAK_CON)
                self.stateMachine(EventType.EVENT_NAK_CON)
            else:
                assert False
        else:
            assert False

    def n_DataBroadcast_Ind(self, message):
        #print "TransportLayerConnected: n_DataBroadcast_Ind"
        message.service = IMI.T_DATA_BROADCAST_IND
        self.post(message)

    def n_DataBroadcast_Con(self, message):
        #print "TransportLayerConnected: n_DataBroadcast_Con", message.confirmed
        message.service = IMI.T_DATA_BROADCAST_CON
        self.post(message)

    def connection_Req(self, tpci, event, source, dest):
        print "TransportLayerConnected: connection_Req: 0x%x" % tpci
        message = MessageBuffer([0] * 7)
        message.service = IMI.N_DATA_INDIVIDUAL_REQ
        frame = message.asStandardFrame()
        frame.tpci = tpci
        frame.source = source
        frame.priority = knx.KNX_OBJ_PRIO_SYSTEM
        self.stateMachine.connectionAddress = dest
        self.stateMachine.sourceAddress = source
        frame.dest = dest
        # KnxTlc_StateMachine(event);
        self.stateMachine(event)
        self.post(message)

    def t_Connect_Req(self, source, dest):
        self.connection_Req(TPCI_CONNECT_REQ_PDU, EventType.EVENT_CONNECT_REQ, source, dest)

    def t_Disconnect_Req(self, source, dest):
        self.connection_Req(TPCI_DISCONNECT_REQ_PDU, EventType.EVENT_DISCONNECT_REQ, source, dest)

    def t_DataConnected_Req(self, message):
        print "TransportLayerConnected: n_DataConnected_Req"
        message.service = IMI.N_DATA_INDIVIDUAL_REQ
        frame = message.asStandardFrame()
        frame.tpci = TPCI_NDT
        self.stateMachine(EventType.EVENT_DATA_CONNECTED_REQ)
        # KnxTlc_StateMachine(KNX_TLC_EVENT_DATA_CONNECTED_REQ);
        self.post(message)

    def t_DataIndividual_Req(self, message):
        #print "TransportLayerConnected: n_DataIndividual_Req"
        message.service = IMI.N_DATA_INDIVIDUAL_REQ
        frame = message.asStandardFrame()
        frame.tpci = TPCI_UDT
        self.post(message)

    def t_DataBroadcast_Req(self, message):
        #print "TransportLayerConnected: n_DataBroadcast_Req"
        message.service = IMI.N_DATA_BROADCAST_REQ
        frame = message.asStandardFrame()
        frame.tpci |= TPCI_UDT
        self.post(message)

    SERVICES = {
        IMI.N_DATA_INDIVIDUAL_IND:  n_DataIndividual_Ind,
        IMI.N_DATA_INDIVIDUAL_CON:  n_DataIndividual_Con,
        IMI.N_DATA_BROADCAST_IND:   n_DataBroadcast_Ind,
        IMI.N_DATA_BROADCAST_CON:   n_DataBroadcast_Con,
        IMI.T_CONNECT_REQ:          t_Connect_Req,
        IMI.T_DISCONNECT_REQ:       t_Disconnect_Req,
        IMI.T_DATA_CONNECTED_REQ:   t_DataConnected_Req,
        IMI.T_DATA_INDIVIDUAL_REQ:  t_DataIndividual_Req,
        IMI.T_DATA_BROADCAST_REQ:   t_DataBroadcast_Req
    }

    SERVICE_GROUP = IMI.TLC_SERVICES

    def initialize(self):
        self.sequenceNumberSend = 0
        self.sequenceNumberReceived = 0
        self.repetitionCount = 0
        self.sequenceNumberOfPDU = 0
        self.state = StateType.STATE_CLOSED

    def ackRervice_Req(self, tpci, source, dest, seqNo):
        message = MessageBuffer([0] * 7)
        message.service = IMI.N_DATA_INDIVIDUAL_REQ
        frame = message.asStandardFrame()
        frame.tpci = tpci | ((SeqNo & 0x0f) << 2)
        frame.source = source
        frame.priority = knx.KNX_OBJ_PRIO_SYSTEM
        frame.dest = dest
        self.post(message)

    def t_Ack_Req(self, source, dest, seqNo):
        self.ackRervice_Req(TPCI_ACK_PDU, source, dest, seqNo)

    def t_Nak_Req(self, source, dest, seqNo):
        self.ackRervice_Req(TPCI_NAK_PDU, source, dest, seqNo)

    def schedule(self, *args):
        """
void KnxTlc_Task(void)
{
    if (KnxTmr_IsRunning(TMR_TIMER_TLC_CON_TIMEOUT) && KnxTmr_IsExpired(TMR_TIMER_TLC_CON_TIMEOUT)) {
        KnxTlc_StateMachine(KNX_TLC_EVENT_TIMEOUT_CON);
    }

    if (KnxTmr_IsRunning(TMR_TIMER_TLC_ACK_TIMEOUT) && KnxTmr_IsExpired(TMR_TIMER_TLC_ACK_TIMEOUT)) {
        KnxTlc_StateMachine(KNX_TLC_EVENT_TIMEOUT_ACK);
    }

    KnxDisp_DispatchLayer(TASK_TC_ID, KnxTlc_ServiceTable);
}
        """

"""
#if KSTACK_MEMORY_MAPPING == STD_ON
STATIC FUNC(void, KSTACK_CODE) T_Connect_ReqSrv(void)
#else
STATIC void T_Connect_ReqSrv(void)
#endif /* KSTACK_MEMORY_MAPPING */
{
    KnxMsg_SetTPCI(KnxMsg_ScratchBufferPtr, KNX_TPCI_UCD);
    KnxMsg_ScratchBufferPtr->service = KNX_SERVICE_N_DATA_INDIVIDUAL_REQ;
    (void)KnxMsg_Post(KnxMsg_ScratchBufferPtr);
}


#if KSTACK_MEMORY_MAPPING == STD_ON
STATIC FUNC(void, KSTACK_CODE) T_Disconnect_ReqSrv(void)
#else
STATIC void T_Disconnect_ReqSrv(void)
#endif /* KSTACK_MEMORY_MAPPING */
{
    KnxMsg_SetTPCI(KnxMsg_ScratchBufferPtr, KNX_TPCI_UCD);
    KnxMsg_ScratchBufferPtr->service = KNX_SERVICE_N_DATA_INDIVIDUAL_REQ;
    (void)KnxMsg_Post(KnxMsg_ScratchBufferPtr);
}
"""

