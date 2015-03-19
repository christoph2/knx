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

from knxReTk.busaccess.nl import NetworkLayer
from knxReTk.busaccess.tlc import TransportLayerConnected
from knxReTk.busaccess.alm import ApplicationManagement
from knxReTk.busaccess.phyTpuart import DataLinkLayer
from knxReTk.utilz.threads import Thread


class Scheduler(object):

    def __init__(self, commServer):
        self.commServer = commServer

    def start(self):
        self.dataLinkLayer = DataLinkLayer()
        self.dataLinkLayer.server = self.commServer
        self.commServer.dataLinkLayer = self.dataLinkLayer
        self.networkLayer = NetworkLayer()
        self.tlc = TransportLayerConnected()
        self.applicationManagement = ApplicationManagement()
        self.commServer.start()

        self.commServer.reset()
        self.commServer.buisyWait()
        self.commServer.getState()
        self.commServer.buisyWait()
        #self.commServer.getProductId()
        #self.commServer.buisyWait()

    def shutdown(self):
        Thread.quitAll()

def scanner():
    for addr in range(0x50, 0x0066):
        print hex(addr)
        mb = MessageBuffer([0xbc, 0xaf, 0xfe] + [bytes.hiByte(addr), bytes.loByte(addr)] + [0x60, 0x80])
        #mb = MessageBuffer([0xbc, 0xaf, 0xfe, 0x00, 0x00, 0x60, 0x80])
        #tlc.n_Connect_Req(0xaffe, addr)
        mb.service = IMI.N_DATA_INDIVIDUAL_REQ
        networkLayer.post(mb)
        commServer.buisyWait()

#scanner()
##
##scheduler = Scheduler(commServer)
##scheduler.start()
##
##scheduler.tlc.t_Connect_Req(0xaffe, 0x0061)
##scheduler.applicationManagement.a_Broadcast_Req(0xaffe, 0x100, [])
##
###print "ETA: ", time.clock() - start
##
##time.sleep(3.0)
##scheduler.shutdown()
##

