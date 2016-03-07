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


import time

from knxReTk.busaccess.tpuart import serialport
from knxReTk.busaccess.phyTpuart import TPUARTServer
from knxReTk.busaccess.scheduler import Scheduler

def main():
    port = serialport.Serial(0, 19200, timeout = 0.1, parity = serialport.Serial.PARITY_EVEN)
    port.connect()
    commServer = TPUARTServer(port)

    scheduler = Scheduler(commServer)
    scheduler.start()

    #scheduler.applicationManagement.a_Broadcast_Req(0xaffe, 0x100, [])
    #scheduler.commServer.buisyWait()
    scheduler.tlc.t_Connect_Req(0xaffe, 0x0061)
    scheduler.commServer.buisyWait()
    time.sleep(.650)
    scheduler.applicationManagement.a_DeviceDescriptor_Read_Req(0xaffe, 0x0061, 0x00)

    scheduler.commServer.buisyWait()
    #scheduler.applicationManagement.a_DeviceDescriptor_Read_Req(0xaffe, 0x0060, 0x00)

    time.sleep(3.0)
    scheduler.shutdown()

if __name__ == '__main__':
    main()

