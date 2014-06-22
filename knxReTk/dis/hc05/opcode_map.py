#!/usr/bin/env python
# -*- coding: utf-8 -*-

__copyright__ = """
   Konnex / EIB Reverserz Toolkit

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

from collections import namedtuple

from knxReTk.utilz.logger import logger
from knxReTk.dis.hc05.operations import load, store

Opcode = namedtuple('Opcode', 'opcode name size cycles addressingMode')

#
#   Adressing modes.
#
NONE    = 0
INH     = 1
IMM     = 2
DIR     = 3
EXT     = 4
REL     = 5
IX      = 6
IX1     = 7
IX2     = 8

OPCODES = [
    Opcode(0x00, "BRSET 0",  3, 5,  DIR),
    Opcode(0x01, "BRCLR 0",  3, 5,  DIR),
    Opcode(0x02, "BRSET 1",  3, 5,  DIR),
    Opcode(0x03, "BRCLR 1",  3, 5,  DIR),
    Opcode(0x04, "BRSET 2",  3, 5,  DIR),
    Opcode(0x05, "BRCLR 2",  3, 5,  DIR),
    Opcode(0x06, "BRSET 3",  3, 5,  DIR),
    Opcode(0x07, "BRCLR 3",  3, 5,  DIR),
    Opcode(0x08, "BRSET 4",  3, 5,  DIR),
    Opcode(0x09, "BRCLR 4",  3, 5,  DIR),
    Opcode(0x0a, "BRSET 5",  3, 5,  DIR),
    Opcode(0x0b, "BRCLR 5",  3, 5,  DIR),
    Opcode(0x0c, "BRSET 6",  3, 5,  DIR),
    Opcode(0x0d, "BRCLR 6",  3, 5,  DIR),
    Opcode(0x0e, "BRSET 7",  3, 5,  DIR),
    Opcode(0x0f, "BRCLR 7",  3, 5,  DIR),

    Opcode(0x10, "BSET 0",   2, 5,  DIR),
    Opcode(0x11, "BCLR 0",   2, 5,  DIR),
    Opcode(0x12, "BSET 1",   2, 5,  DIR),
    Opcode(0x13, "BCLR 1",   2, 5,  DIR),
    Opcode(0x14, "BSET 2",   2, 5,  DIR),
    Opcode(0x15, "BCLR 2",   2, 5,  DIR),
    Opcode(0x16, "BSET 3",   2, 5,  DIR),
    Opcode(0x17, "BCLR 3",   2, 5,  DIR),
    Opcode(0x18, "BSET 4",   2, 5,  DIR),
    Opcode(0x19, "BCLR 4",   2, 5,  DIR),
    Opcode(0x1a, "BSET 5",   2, 5,  DIR),
    Opcode(0x1b, "BCLR 5",   2, 5,  DIR),
    Opcode(0x1c, "BSET 6",   2, 5,  DIR),
    Opcode(0x1d, "BCLR 6",   2, 5,  DIR),
    Opcode(0x1e, "BSET 7",   2, 5,  DIR),
    Opcode(0x1f, "BCLR 7",   2, 5,  DIR),

    Opcode(0x20, "BRA",      2, 3,  REL),
    Opcode(0x21, "BRN",      2, 3,  REL),
    Opcode(0x22, "BHI",      2, 3,  REL),
    Opcode(0x23, "BLS",      2, 3,  REL),
    Opcode(0x24, "BCC",      2, 3,  REL),
    Opcode(0x25, "BCS",      2, 3,  REL),
    Opcode(0x26, "BNE",      2, 3,  REL),
    Opcode(0x27, "BEQ",      2, 3,  REL),
    Opcode(0x28, "BHCC",     2, 3,  REL),
    Opcode(0x29, "BHCS",     2, 3,  REL),
    Opcode(0x2a, "BPL",      2, 3,  REL),
    Opcode(0x2b, "BMI",      2, 3,  REL),
    Opcode(0x2c, "BMC",      2, 3,  REL),
    Opcode(0x2d, "BMS",      2, 3,  REL),
    Opcode(0x2e, "BIL",      2, 3,  REL),
    Opcode(0x2f, "BIH",      2, 3,  REL),

    Opcode(0x30, "NEG",      2, 5,  DIR),
    Opcode(0x31, "",         0, 0,  DIR),
    Opcode(0x32, "",         0, 0,  DIR),
    Opcode(0x33, "COM",      2, 5,  DIR),
    Opcode(0x34, "LSR",      2, 5,  DIR),
    Opcode(0x35, "",         0, 0,  DIR),
    Opcode(0x36, "ROR",      2, 5,  DIR),
    Opcode(0x37, "ASR",      2, 5,  DIR),
    Opcode(0x38, "ASL",      2, 5,  DIR),
    Opcode(0x39, "ROL",      2, 5,  DIR),
    Opcode(0x3a, "DEC",      2, 5,  DIR),
    Opcode(0x3b, "",         0, 0,  DIR),
    Opcode(0x3c, "INC",      2, 5,  DIR),
    Opcode(0x3d, "TST",      2, 4,  DIR),
    Opcode(0x3e, "",         0, 0,  DIR),
    Opcode(0x3f, "CLR",      2, 5,  DIR),

    Opcode(0x40, "NEGA",     1, 3,  INH),
    Opcode(0x41, "",         0, 0,  INH),
    Opcode(0x42, "MUL",      1, 11, INH),
    Opcode(0x43, "COMA",     1, 3,  INH),
    Opcode(0x44, "LSRA",     1, 3,  INH),
    Opcode(0x45, "",         0, 0,  NONE),
    Opcode(0x46, "RORA",     1, 3,  INH),
    Opcode(0x47, "ASRA",     1, 3,  INH),
    Opcode(0x48, "ASLA",     1, 3,  INH),
    Opcode(0x49, "ROLA",     1, 3,  INH),
    Opcode(0x4a, "DECA",     1, 3,  INH),
    Opcode(0x4b, "",         0, 0,  INH),
    Opcode(0x4c, "INCA",     1, 3,  INH),
    Opcode(0x4d, "TSTA",     1, 3,  INH),
    Opcode(0x4e, "",         0, 0,  NONE),
    Opcode(0x4f, "CLRA",     1, 3,  INH),

    Opcode(0x50, "NEGX",     1, 3,  INH),
    Opcode(0x51, "",         0, 0,  NONE),
    Opcode(0x52, "",         0, 0,  NONE),
    Opcode(0x53, "COMX",     1, 3,  INH),
    Opcode(0x54, "LSRA",     1, 3,  INH),
    Opcode(0x55, "",         0, 0,  NONE),
    Opcode(0x56, "RORX",     1, 3,  INH),
    Opcode(0x57, "ASRX",     1, 3,  INH),
    Opcode(0x58, "ASLX",     1, 3,  INH),
    Opcode(0x59, "ROLX",     1, 3,  INH),
    Opcode(0x5a, "DECX",     1, 3,  INH),
    Opcode(0x5b, "",         0, 0,  NONE),
    Opcode(0x5c, "INCX",     1, 3,  INH),
    Opcode(0x5d, "TSTX",     1, 3,  INH),
    Opcode(0x5e, "",         0, 0,  NONE),
    Opcode(0x5f, "CLRX",     1, 3,  INH),

    Opcode(0x60, "NEG",      2, 6,  IX1),
    Opcode(0x61, "",         0, 0,  NONE),
    Opcode(0x62, "",         0, 0,  IX1),
    Opcode(0x63, "COM",      2, 6,  IX1),
    Opcode(0x64, "LSR",      2, 6,  IX1),
    Opcode(0x65, "",         0, 0,  NONE),
    Opcode(0x66, "ROR",      2, 6,  IX1),
    Opcode(0x67, "ASR",      2, 6,  IX1),
    Opcode(0x68, "ASL",      2, 6,  IX1),
    Opcode(0x69, "ROL",      2, 6,  IX1),
    Opcode(0x6a, "DEC",      2, 6,  IX1),
    Opcode(0x6b, "",         0, 0,  NONE),
    Opcode(0x6c, "INC",      2, 6,  IX1),
    Opcode(0x6d, "TST",      2, 5,  IX1),
    Opcode(0x6e, "",         0, 0,  NONE),
    Opcode(0x6f, "CLR",      2, 6,  IX1),

    Opcode(0x70, "NEG",      1, 5,  IX),
    Opcode(0x71, "",         0, 0,  NONE),
    Opcode(0x72, "",         0, 0,  NONE),
    Opcode(0x73, "COM",      1, 5,  IX),
    Opcode(0x74, "LSR",      1, 5,  IX),
    Opcode(0x75, "",         0, 0,  NONE),
    Opcode(0x76, "ROR",      1, 5,  IX),
    Opcode(0x77, "ASR",      1, 5,  IX),
    Opcode(0x78, "ASL",      1, 5,  IX),
    Opcode(0x79, "ROL",      1, 5,  IX),
    Opcode(0x7a, "DEC",      1, 5,  IX),
    Opcode(0x7b, "",         0, 0,  NONE),
    Opcode(0x7c, "INC",      1, 5,  IX),
    Opcode(0x7d, "TST",      1, 4,  IX),
    Opcode(0x7e, "",         0, 0,  NONE),
    Opcode(0x7f, "CLR",      1, 5,  IX),

    Opcode(0x80, "RTI",      1, 9,  INH),
    Opcode(0x81, "RTS",      1, 6,  INH),
    Opcode(0x82, "",         0, 0,  NONE),
    Opcode(0x83, "SWI",      1, 10, INH),
    Opcode(0x84, "",         0, 0,  NONE),
    Opcode(0x85, "",         0, 0,  NONE),
    Opcode(0x86, "",         0, 0,  NONE),
    Opcode(0x87, "",         0, 0,  NONE),
    Opcode(0x88, "",         0, 0,  NONE),
    Opcode(0x89, "",         0, 0,  NONE),
    Opcode(0x8a, "",         0, 0,  NONE),
    Opcode(0x8b, "",         0, 0,  NONE),
    Opcode(0x8c, "",         0, 0,  NONE),
    Opcode(0x8d, "",         0, 0,  NONE),
    Opcode(0x8e, "STOP",     1, 2,  INH),
    Opcode(0x8f, "WAIT",     1, 2,  INH),

    Opcode(0x90, "",         0, 0,  NONE),
    Opcode(0x91, "",         0, 0,  NONE),
    Opcode(0x92, "",         0, 0,  NONE),
    Opcode(0x93, "",         0, 0,  NONE),
    Opcode(0x94, "",         0, 0,  NONE),
    Opcode(0x95, "",         0, 0,  NONE),
    Opcode(0x96, "",         0, 0,  NONE),
    Opcode(0x97, "TAX",      1, 2,  INH),
    Opcode(0x98, "CLC",      1, 2,  INH),
    Opcode(0x99, "SEC",      1, 2,  INH),
    Opcode(0x9a, "CLI",      1, 2,  INH),
    Opcode(0x9b, "SEI",      1, 2,  INH),
    Opcode(0x9c, "RSP",      1, 2,  INH),
    Opcode(0x9d, "NOP",      1, 2,  INH),
    Opcode(0x9e, "",         0, 0,  NONE),
    Opcode(0x9f, "TXA",      1, 2,  INH),

    Opcode(0xa0, "SUB",      2, 2,  IMM),
    Opcode(0xa1, "CMP",      2, 2,  IMM),
    Opcode(0xa2, "SBC",      2, 2,  IMM),
    Opcode(0xa3, "CPX",      2, 2,  IMM),
    Opcode(0xa4, "AND",      2, 2,  IMM),
    Opcode(0xa5, "BIT",      2, 2,  IMM),
    Opcode(0xa6, "LDA",      2, 2,  IMM),
    Opcode(0xa7, "",         0, 0,  NONE),
    Opcode(0xa8, "EOR",      2, 2,  IMM),
    Opcode(0xa9, "ADC",      2, 2,  IMM),
    Opcode(0xaa, "ORA",      2, 2,  IMM),
    Opcode(0xab, "ADD",      2, 2,  IMM),
    Opcode(0xac, "",         0, 0,  NONE),
    Opcode(0xad, "BSR",      2, 6,  REL),
    Opcode(0xae, "LDX",      2, 2,  IMM),
    Opcode(0xaf, "",         0, 0,  NONE),

    Opcode(0xb0, "SUB",      2, 3,  DIR),
    Opcode(0xb1, "CMP",      2, 3,  DIR),
    Opcode(0xb2, "SBC",      2, 3,  DIR),
    Opcode(0xb3, "CPX",      2, 3,  DIR),
    Opcode(0xb4, "AND",      2, 3,  DIR),
    Opcode(0xb5, "BIT",      2, 3,  DIR),
    Opcode(0xb6, "LDA",      2, 3,  DIR),
    Opcode(0xb7, "STA",      2, 4,  DIR),
    Opcode(0xb8, "EOR",      2, 3,  DIR),
    Opcode(0xb9, "ADC",      2, 3,  DIR),
    Opcode(0xba, "ORA",      2, 3,  DIR),
    Opcode(0xbb, "ADD",      2, 3,  DIR),
    Opcode(0xbc, "JMP",      2, 2,  DIR),
    Opcode(0xbd, "JSR",      2, 5,  DIR),
    Opcode(0xbe, "LDX",      2, 3,  DIR),
    Opcode(0xbf, "STX",      2, 4,  DIR),

    Opcode(0xc0, "SUB",      3, 4,  EXT),
    Opcode(0xc1, "CMP",      3, 4,  EXT),
    Opcode(0xc2, "SBC",      3, 4,  EXT),
    Opcode(0xc3, "CPX",      3, 4,  EXT),
    Opcode(0xc4, "AND",      3, 4,  EXT),
    Opcode(0xc5, "BIT",      3, 4,  EXT),
    Opcode(0xc6, "LDA",      3, 4,  EXT),
    Opcode(0xc7, "STA",      3, 5,  EXT),
    Opcode(0xc8, "EOR",      3, 4,  EXT),
    Opcode(0xc9, "ADC",      3, 4,  EXT),
    Opcode(0xca, "ORA",      3, 4,  EXT),
    Opcode(0xcb, "ADD",      3, 4,  EXT),
    Opcode(0xcc, "JMP",      3, 3,  EXT),
    Opcode(0xcd, "JSR",      3, 6,  EXT),
    Opcode(0xce, "LDX",      3, 4,  EXT),
    Opcode(0xcf, "STX",      3, 5,  EXT),

    Opcode(0xd0, "SUB",      3, 5,  IX2),
    Opcode(0xd1, "CMP",      3, 5,  IX2),
    Opcode(0xd2, "SBC",      3, 5,  IX2),
    Opcode(0xd3, "CPX",      3, 5,  IX2),
    Opcode(0xd4, "AND",      3, 5,  IX2),
    Opcode(0xd5, "BIT",      3, 5,  IX2),
    Opcode(0xd6, "LDA",      3, 5,  IX2),
    Opcode(0xd7, "STA",      3, 6,  IX2),
    Opcode(0xd8, "EOR",      3, 5,  IX2),
    Opcode(0xd9, "ADC",      3, 5,  IX2),
    Opcode(0xda, "ORA",      3, 5,  IX2),
    Opcode(0xdb, "ADD",      3, 5,  IX2),
    Opcode(0xdc, "JMP",      3, 4,  IX2),
    Opcode(0xdd, "JSR",      3, 7,  IX2),
    Opcode(0xde, "LDX",      3, 5,  IX2),
    Opcode(0xdf, "STX",      3, 6,  IX2),

    Opcode(0xe0, "SUB",      2, 4,  IX1),
    Opcode(0xe1, "CMP",      2, 4,  IX1),
    Opcode(0xe2, "SBC",      2, 4,  IX1),
    Opcode(0xe3, "CPX",      2, 4,  IX1),
    Opcode(0xe4, "AND",      2, 4,  IX1),
    Opcode(0xe5, "BIT",      2, 4,  IX1),
    Opcode(0xe6, "LDA",      2, 4,  IX1),
    Opcode(0xe7, "STA",      2, 5,  IX1),
    Opcode(0xe8, "EOR",      2, 4,  IX1),
    Opcode(0xe9, "ADC",      2, 4,  IX1),
    Opcode(0xea, "ORA",      2, 4,  IX1),
    Opcode(0xeb, "ADD",      2, 4,  IX1),
    Opcode(0xec, "JMP",      2, 3,  IX1),
    Opcode(0xed, "JSR",      2, 6,  IX1),
    Opcode(0xee, "LDX",      2, 4,  IX1),
    Opcode(0xef, "STX",      2, 5,  IX1),

    Opcode(0xf0, "SUB",      1, 3,  IX),
    Opcode(0xf1, "CMP",      1, 3,  IX),
    Opcode(0xf2, "SBC",      1, 3,  IX),
    Opcode(0xf3, "CPX",      1, 3,  IX),
    Opcode(0xf4, "AND",      1, 3,  IX),
    Opcode(0xf5, "BIT",      1, 3,  IX),
    Opcode(0xf6, "LDA",      1, 3,  IX),
    Opcode(0xf7, "STA",      1, 4,  IX),
    Opcode(0xf8, "EOR",      1, 3,  IX),
    Opcode(0xf9, "ADC",      1, 3,  IX),
    Opcode(0xfa, "ORA",      1, 3,  IX),
    Opcode(0xfb, "ADD",      1, 3,  IX),
    Opcode(0xfc, "JMP",      1, 2,  IX),
    Opcode(0xfd, "JSR",      1, 5,  IX),
    Opcode(0xfe, "LDX",      1, 3,  IX),
    Opcode(0xff, "STX",      1, 4,  IX),
]

ILLEGAL_OPCODES = [
    0x31, 0x32, 0x35, 0x3b, 0x3e, 0x41, 0x45, 0x4b, 0x4e, 0x51, 0x52, 0x55,
    0x5b, 0x5e, 0x61, 0x62, 0x65, 0x6b, 0x6e, 0x71, 0x72, 0x35, 0x7b, 0x7e,
    0x82, 0x84, 0x85, 0x86, 0x87, 0x88, 0x89, 0x8a, 0x8b, 0x8c, 0x8d, 0x90,
    0x91, 0x93, 0x94, 0x95, 0x96, 0x9e, 0xa7, 0xac, 0xaf
]

##
## The following categorizations are only relevant for disassembling.
##
CALLS = (
    0xad, 0xbd, 0xcd, 0xdd, 0xed, 0xfd
)

JUMPS = (
    0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b,
    0x0c, 0x0d, 0x0e, 0x0f, 0x20, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27,
    0x28, 0x29, 0x2a, 0x2b, 0x2c, 0x2d, 0x2e, 0x2f,

    0xbc, 0xcc, 0xdc, 0xec, 0xfc
)

RETURNS = (
    0x80, 0x81,
    0x20, # BRA
    0xbc, 0xcc, 0xdc, 0xec, 0xfc    # Unconditional Jumps.
)

