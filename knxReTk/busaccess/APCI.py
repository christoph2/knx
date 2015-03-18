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

from knxReTk.utilz.classes import SingletonBase

class APCIType(SingletonBase):
    APCI_GROUP_VALUE_READ           = 0     # Multicast.
    APCI_GROUP_VALUE_RESP           = 1
    APCI_GROUP_VALUE_WRITE          = 2

    APCI_INDIVIDUAL_ADDRESS_WRITE   = 3     # Broadcast.
    APCI_INDIVIDUAL_ADDRESS_READ    = 4
    APCI_INDIVIDUAL_ADDRESS_RESP    = 5

    APCI_ADC_READ                   = 6     # P2P-Connection-Oriented.
    APCI_ADC_RESP                   = 7
    APCI_MEMORY_READ                = 8
    APCI_MEMORY_RESP                = 9
    APCI_MEMORY_WRITE               = 10

    APCI_USER_MSG                   = 11    # User-defined Messages.

    APCI_DEVICE_DESCRIPTOR_READ     = 12    # P2P-Conection-Less.
    APCI_DEVICE_DESCRIPTOR_RESP     = 13

    APCI_RESTART                    = 14    # P2P-Connection-Oriented.

    APCI_ESCAPE                     = 15    # Others, escape.

    _VALUES = {
        APCI_GROUP_VALUE_READ:          'APCI_GROUP_VALUE_READ',
        APCI_GROUP_VALUE_RESP:          'APCI_GROUP_VALUE_RESP',
        APCI_GROUP_VALUE_WRITE:         'APCI_GROUP_VALUE_WRITE',
        APCI_INDIVIDUAL_ADDRESS_WRITE:  'APCI_INDIVIDUAL_ADDRESS_WRITE',
        APCI_INDIVIDUAL_ADDRESS_READ:   'APCI_INDIVIDUAL_ADDRESS_READ',
        APCI_INDIVIDUAL_ADDRESS_RESP:   'APCI_INDIVIDUAL_ADDRESS_RESP',
        APCI_ADC_READ:                  'APCI_ADC_READ',
        APCI_ADC_RESP:                  'APCI_ADC_RESP',
        APCI_MEMORY_READ:               'APCI_MEMORY_READ',
        APCI_MEMORY_RESP:               'APCI_MEMORY_RESP',
        APCI_MEMORY_WRITE:              'APCI_MEMORY_WRITE',
        APCI_USER_MSG:                  'APCI_USER_MSG',
        APCI_DEVICE_DESCRIPTOR_READ:    'APCI_DEVICE_DESCRIPTOR_READ',
        APCI_DEVICE_DESCRIPTOR_RESP:    'APCI_DEVICE_DESCRIPTOR_RESP',
        APCI_RESTART:                   'APCI_RESTART',
        APCI_ESCAPE:                    'APCI_ESCAPE',
    }

    @classmethod
    def toString(klass, value):
        return klass._VALUES.get(value, '<INVALID>')


# Group-Services.
A_GROUPVALUE_READ                      = 0x000
A_GROUPVALUE_RESPONSE                  = 0x040
A_GROUPVALUE_WRITE                     = 0x080

# Broadcast.
A_PHYSICALADDRESS_WRITE                = 0x0C0   # Phys.AddrSet
A_PHYSICALADDRESS_READ                 = 0x100   # Phys.AddrRead
A_PHYSICALADDRESS_RESPONSE             = 0x140   # Phys.AddrResponse

# Point-to-Point.
A_ADC_READ                             = 0x180   # ADCRead
A_ADC_RESPONSE                         = 0x1C0   # ADCResponse
A_MEMORY_READ                          = 0x200   # MemoryRead
A_MEMORY_RESPONSE                      = 0x240   # MemoryResponse
A_MEMORY_WRITE                         = 0x280   # MemoryWrite

A_USERMEMORY_READ                      = 0x2C0   # UserDataRead
A_USERMEMORY_RESPONSE                  = 0x2C1   # UserDataResponse
A_USERMEMORY_WRITE                     = 0x2C2   # UserDataWrite
A_USERMEMORYBIT_WRITE                  = 0x2C4   # UserDataBitWrite
A_USERMANUFACTURERINFO_READ            = 0x2C5   # UserMgmtTypeRead
A_USERMANUFACTURERINFO_RESPONSE        = 0x2C6   # UserMgmtTypeResponse

# Reserved for USERMSGs: 0x2C7 - 2F7 (48 Codes).
# Reserved for manufacturer specific msgs: 0x2F8 - 2FE (6 Codes).

A_DEVICEDESCRIPTOR_READ                = 0x300   # MaskVersionRead
A_DEVICEDESCRIPTOR_RESPONSE            = 0x340   # MaskVersionResponse
A_RESTART                              = 0x380   # Restart

# Coupler-/Router-specific.
A_OPEN_ROUTING_TABLE_REQ               = 0x3C0   # LcTabMemEnable
A_READ_ROUTING_TABLE_REQ               = 0x3C1   # LcTabMemRead
A_READ_ROUTING_TABLE_RES               = 0x3C2   # LcTabMemResponse
A_WRITE_ROUTING_TABLE_REQ              = 0x3C3   # LcTabMemWrite
A_READ_ROUTER_MEMORY_REQ               = 0x3C8   # LcSlaveRead
A_READ_ROUTER_MEMORY_RES               = 0x3C9   # LcSlaveResponse
A_WRITE_ROUTER_MEMORY_REQ              = 0x3CA   # LcSlaveWrite
A_READ_ROUTER_STATUS_REQ               = 0x3CD   # LcGroupRead
A_READ_ROUTER_STATUS_RES               = 0x3CE   # LcGroupResponse
A_WRITE_ROUTER_STATUS_REQ              = 0x3CF   # LcGroupWrite

A_MEMORYBIT_WRITE                      = 0x3D0   # BitWrite
A_AUTHORIZE_REQUEST                    = 0x3D1   # AuthorizeRequest
A_AUTHORIZE_RESPONSE                   = 0x3D2   # AuthorizeResponse
A_KEY_WRITE                            = 0x3D3   # SetKeyRequest
A_KEY_RESPONSE                         = 0x3D4   # SetKeyResponse

A_PROPERTYVALUE_READ                   = 0x3D5   # PropertyRead
A_PROPERTYVALUE_RESPONSE               = 0x3D6   # PropertyResponse
A_PROPERTYVALUE_WRITE                  = 0x3D7   # PropertyWrite
A_PROPERTYDESCRIPTION_READ             = 0x3D8   # PropertyDescriptionRead
A_PROPERTYDESCRIPTION_RESPONSE         = 0x3D9   # PropertyDescriptionResponse

# Broadcast.
A_PHYSICALADDRESSSERIALNUMBER_READ     = 0x3DC   # PhysAddrSerNoRead
A_PHYSICALADDRESSSERIALNUMBER_RESPONSE = 0x3DD   # PhysAddrSerNoResponse
A_PHYSICALADDRESSSERIALNUMBER_WRITE    = 0x3DE   # PhysAddrSerNoWrite
A_SERVICEINFORMATION_INDICATION_WRITE  = 0x3DF   # ServiceInfo

A_DOMAINADDRESS_WRITE                  = 0x3E0   # SysIdWrite
A_DOMAINADDRESS_READ                   = 0x3E1   # SysIdRead
A_DOMAINADDRESS_RESPONSE               = 0x3E2   # SysIdResponse
A_DOMAINADDRESSSELECTIVE_READ          = 0x3E3   # SysIdSelectiveRead

A_NETWORKPARAMETER_WRITE               = 0x3E4   # A_NetworkParameter_Write (s. Supplement S09).
A_NETWORKPARAMETER_READ                = 0x3DA   # (s. Supplement S03).
A_NETWORKPARAMETER_RESPONSE            = 0x3DB

# Point to Point.
A_LINK_READ                            = 0x3E5
A_LINK_RESPONSE                        = 0x3E6
A_LINK_WRITE                           = 0x3E7

# Multicast.
A_GROUPPROPVALUE_READ                  = 0x3E8
A_GROUPPROPVALUE_RESPONSE              = 0x3E9
A_GROUPPROPVALUE_WRITE                 = 0x3EA
A_GROUPPROPVALUE_INFOREPORT            = 0x3EB # s. KNX 10_01 Logical Tag Extended.

