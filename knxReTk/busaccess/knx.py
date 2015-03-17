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

##
##  Frame-Types.
##
FRAME_EXTENDED = 0x00
FRAME_STANDARD = 0x80
FRAME_POLLING  = 0xC0

##
##  Global defines.
##
IAK_OK                  = 0x00
IAK_NOT_OK              = 0x01

##
##  RunError-Codes.
##
KNX_RUNERROR_SYS3_ERR   = 0x40  # internal system error (not for each default MCB [ROM] an
                                # MCB [EEPROM] exists with the same start address)
KNX_RUNERROR_SYS2_ERR   = 0x20  # internal system error (stuck/ overheat detection).
KNX_RUNERROR_OBJ_ERR    = 0x10  # RAM flag table error (*PTR not in ZPAGE range).
KNX_RUNERROR_STK_OVL    = 0x08  # stack overflow was detected.
KNX_RUNERROR_EEPROM_ERR = 0x04  # EEPROM check detected an CRC error.
KNX_RUNERROR_SYS1_ERR   = 0x02  # internal system error (parity bit in SystemState is corrupt).
KNX_RUNERROR_SYS0_ERR   = 0x01  # internal system error (msg buffer offset corrupt).

##
##  Config-Byte / Object-Descriptor.
##
KNX_OBJ_UPDATE_ENABLE   = 0x80  # GroupValueRead()_Res wird verarbeitet - nur Mask 0020h, 0021h.
KNX_OBJ_TRANSMIT_ENABLE = 0x40  # Lese- und Schreib-Anforderungen (Requests) vom App.-Layer werden verarbeitet.
KNX_OBJ_EEPROM_VALUE    = 0x20  # Objektwert steht im EEPROM (statt im RAM).
KNX_OBJ_WRITE_ENABLE    = 0x10  # Objektwert kann über den Bus geschrieben werden.
KNX_OBJ_READ_ENABLE     = 0x08  # Objektwert kann über den Bus gelesen werden.
KNX_OBJ_COMM_ENABLE     = 0x04  # "Mainswitch" for Communikation.

##
##  Config-Byte / Priorities.
##
KNX_OBJ_PRIO_SYSTEM     = 0
KNX_OBJ_PRIO_URGENT     = 2
KNX_OBJ_PRIO_NORMAL     = 1
KNX_OBJ_PRIO_LOW        = 3

##
##  Comm-Flags.
##
KNX_OBJ_UPDATED                 = 0x08
KNX_OBJ_DATA_REQUEST            = 0x04

##
##  Transmission-Status
##
KNX_OBJ_IDLE_OK                 = 0x00
KNX_OBJ_IDLE_ERROR              = 0x01
KNX_OBJ_TRANSMITTING            = 0x02
KNX_OBJ_TRANSMIT_REQ            = 0x03

BCU20_PRIVILEGE_CONFIGURATION   = 0
BCU20_PRIVILEGE_SERVICE         = 1
BCU20_PRIVILEGE_USER            = 2
BCU20_PRIVILEGE_NO              = 3

KNX_UNUSED_TSAP                 = 0xfe
KNX_INVALID_TSAP                = 0x00


##
##  Supported Bus Interfaces.
##
KNX_BIF_TPUART_1                        = 0
KNX_BIF_TPUART_2                        = 1
KNX_BIF_TPUART_NCN5120                  = 2

##
##  Power supply of controller module.
##
KNX_MODULE_POWER_BY_BUS                 = 0
KNX_MODULE_POWER_BY_AUXILIARY_SUPPLY    = 1

##
##
##
KNX_LITTLE_ENDIAN                       = 0
KNX_BIG_ENDIAN                          = 1

