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


from knxReTk.busaccess.layer import Layer
from knxReTk.busaccess.imi import IMI

CONF_OK         = 0x00
CONF_ERROR      = 0x01

IndicationServices = (
    IMI.N_DATA_BROADCAST_IND,
    IMI.N_DATA_GROUP_IND,
    IMI.N_DATA_INDIVIDUAL_IND
)

ConfirmationServices = (
    IMI.N_DATA_BROADCAST_CON,
    IMI.N_DATA_GROUP_CON,
    IMI.N_DATA_INDIVIDUAL_CON
)

class NetworkLayer(Layer):

    def l_Data_Ind(self, message):
        #print "l_Data_Ind", message
        self.dispatchIncoming(message, IndicationServices)

    def l_Data_Con(self, message):
        #print "l_Data_Con", message
        self.dispatchIncoming(message, ConfirmationServices)

    def l_PollData_Con(self, message):
        print "l_PollData_Con", message

    def l_Busmon_Ind(self, message):
        print "l_Busmon_Ind", message

    def n_DataIndividual_Req(self, message):
        #print "n_DataIndividual_Req", message
        frame = message.asStandardFrame()
        frame.addressType = frame.DAF_INDIVIDUAL
        frame.setRoutingCount()
        message.service = IMI.L_DATA_REQ
        self.post(message)

    def n_DataGroup_Req(self, message):
        print "n_DataGroup_Req", message
        frame = message.asStandardFrame()
        frame.addressType = frame.DAF_MULTICAST
        frame.setRoutingCount()
        message.service = IMI.L_DATA_REQ
        self.post(message)

    def n_DataBroadcast_Req(self, message):
        frame = message.asStandardFrame()
        frame.addressType = frame.DAF_MULTICAST
        frame.setRoutingCount()
        message.service = IMI.L_DATA_REQ
        self.post(message)
        #print "n_DataBroadcast_Req", message

    def n_PollData_Req(self, message):
        print "n_PollData_Req", message

    SERVICES = {
        IMI.L_DATA_IND:            l_Data_Ind,
        IMI.L_DATA_CON:            l_Data_Con,
        IMI.L_POLL_DATA_CON:       l_PollData_Con,
        IMI.L_BUSMON_IND:          l_Busmon_Ind,
        IMI.N_DATA_INDIVIDUAL_REQ: n_DataIndividual_Req,
        IMI.N_DATA_GROUP_REQ:      n_DataGroup_Req,
        IMI.N_DATA_BROADCAST_REQ:  n_DataBroadcast_Req,
        IMI.N_POLL_DATA_REQ:       n_PollData_Req,
    }

    SERVICE_GROUP = IMI.NL_SERVICES

    #counter = 0

    def dispatchIncoming(self, message, services):
        #self.counter += 1
        frame = message.asStandardFrame()
        if frame.isMulticastAddressed:
            print "NetworkLayer: Multicast_Ind", message.confirmed
            if frame.dest == 0x0000:
                # Broadcast-Communication.
                message.service = services[0]
            else:
                message.service = services[1]
        else:
            if message.confirmed:
                print "NetworkLayer: Indivual_Ind", hex(frame.dest),
            message.service = services[2]
        self.post(message)

"""
STATIC void KnxNl_CheckRoutingCount(KnxMsg_BufferPtr pBuffer)
{
    if (KnxMsg_GetRoutingCount(pBuffer) == MSG_NO_ROUTING_CTRL) {
        KnxMsg_SetRoutingCtrl(pBuffer, TRUE);
    } else {
        KnxMsg_SetRoutingCtrl(pBuffer, FALSE);
    }
}
"""

