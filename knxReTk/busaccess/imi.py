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


class IMI(object):

##
##  Service Groups.
##
    LL_SERVICES     = 0x10
    NL_SERVICES     = 0x20
    TLG_SERVICES    = 0x30
    TLC_SERVICES    = 0x40
    ALG_SERVICES    = 0x70
    ALM_SERVICES    = 0x80

##
##  Link-Layer.
##

    L_DATA_REQ              = 0x10
    L_POLL_DATA_REQ         = 0x11

##
##  Network-Layer.
##
    L_DATA_IND              = 0x20
    L_DATA_CON              = 0x21
    L_POLL_DATA_CON         = 0x22
    L_BUSMON_IND            = 0x23
    N_DATA_INDIVIDUAL_REQ   = 0x24
    N_DATA_GROUP_REQ        = 0x25
    N_DATA_BROADCAST_REQ    = 0x26
    N_POLL_DATA_REQ         = 0x27

##
##  Transport-Layer/group-oriented.
##
    N_DATA_GROUP_IND        = 0x30
    N_DATA_GROUP_CON        = 0x31
    N_POLL_DATA_CON         = 0x32
    T_DATA_GROUP_REQ        = 0x33
    T_POLL_DATA_REQ         = 0x34

##
##  Transport-Layer/connection-oriented.
##
    N_DATA_INDIVIDUAL_IND   = 0x40
    N_DATA_INDIVIDUAL_CON   = 0x41
    N_DATA_BROADCAST_IND    = 0x42
    N_DATA_BROADCAST_CON    = 0x43
    T_CONNECT_REQ           = 0x44
    T_DISCONNECT_REQ        = 0x45
    T_DATA_CONNECTED_REQ    = 0x46
    T_DATA_INDIVIDUAL_REQ   = 0x47
    T_DATA_BROADCAST_REQ    = 0x48

##
##  Application-Layer/group-oriented.
##
    T_DATA_GROUP_IND        = 0x70
    T_DATA_GROUP_CON        = 0x71
    T_POLL_DATA_CON         = 0x72
    A_DATA_GROUP_REQ        = 0x73
    A_POLL_DATA_REQ         = 0x74

##
##  Application-Layer/managment-part.
##
    T_CONNECT_IND           = 0x80
    T_CONNECT_CON           = 0x81
    T_DISCONNECT_IND        = 0x82
    T_DISCONNECT_CON        = 0x83
    T_DATA_CONNECTED_IND    = 0x84
    T_DATA_CONNECTED_CON    = 0x85
    T_DATA_INDIVIDUAL_IND   = 0x86
    T_DATA_INDIVIDUAL_CON   = 0x87
    T_DATA_BROADCAST_IND    = 0x88
    T_DATA_BROADCAST_CON    = 0x89

