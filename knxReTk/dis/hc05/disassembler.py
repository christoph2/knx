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

import os
from pprint import pprint
import sys

from knxReTk.utilz.logger import logger
from knxReTk.executionModel.memory import ReadWriteMemory
from knxReTk.dis.explorer import MemoryExplorer
from knxReTk.dis.hc05.opcode_map import OPCODES, ILLEGAL_OPCODES, CALLS, JUMPS, RETURNS
import knxReTk.dis.hc05.opcode_map as opcode_map
from knxReTk.config.symbols import Symbols
from knxReTk.utilz.config import readConfigData

class Entry(object):

    def __init__(self, address, size):
        self._address = address
        self._size = size

    @property
    def address(self):
        return self._address

    @property
    def size(self):
        return self._size


class OperationList(list):
    addresses = set()

    def append(self, value):
        if not value.address in self.addresses:
            self.addresses.add(value.address)
            super(OperationList, self).append(value)
            #print str(self)
        #else:
        #    print "*** Already inserted: '0x%04x'" % value.address

    def extend(self, container):
        for item in container:
            self.append(item)
        #print "List size after extend: %u" % len(self)

    def __contains__(self, other):
        return other.address in self.addresses

    def __str__(self):
        return "<%s [%s] >" % (self.__class__.__name__, [v.address for v in self])

    __repr__ = __str__


class Operation(Entry):

    METHODS = {
        opcode_map.INH: "inherent",
        opcode_map.IMM: "immediate",
        opcode_map.DIR: "direct",
        opcode_map.EXT: "extended",
        opcode_map.REL: "relative",
        opcode_map.IX:  "indexed",
        opcode_map.IX1: "indexedOne",
        opcode_map.IX2: "indexedTwo",
    }

    def __init__(self, address, size, label, opcode, opcodeName, operand, operandData, addressingMode, comment):
        super(Operation, self).__init__(address, size)
        self.label = label
        self.opcode = opcode
        self.opcodeName = opcodeName
        self.operand = operand
        self.operandData = operandData
        self.addressingMode = addressingMode
        self.comment = comment

    def __hash__(self):
        return hash(self.address)


    def __str__(self):
        displayString, _ = self.processes()
        return "$%04x %02x %s    %-20s %s %s" % (
            self.address, self.opcode, self.formatOperandData(), self.label, self.opcodeName, displayString
        )

    __repr__ = __str__

    def formatOperandData(self):
        if self.operandData:
            if self.operandData > 0xff:
                return "%02x %02x" % ((self.operandData & 0xff00) >> 8, (self.operandData & 0xff), )
            else:
                return "%02x   " % self.operandData
        else:
            return "     "

    def inherent(self):
        return ("", None)

    def immediate(self):
        operand = '#%02x' % self.operandData
        return (operand, None)

    def direct(self):
        if (self.opcode < 0x10):        # BRSET/BRCLR
            op0 = (self.operandData & 0xff00) >> 8  # TODO: wordToBytes Fct.
            op1 = self.operandData & 0xff
            if op1 >= 0x80:
                relativeBranchOffset = (0xff & (op1 * -1) - 3) * -1
            else:
                relativeBranchOffset = op1 + 3
            destination = self.address + relativeBranchOffset
            operand = "%s, $%04x" % (self.getLocationDir(op0), destination)
            # FIXME: Sprung-Behandlung.
        elif (self.opcode < 0x20):      # BSET/BCLR
            operand = "%s" % self.getLocationDir(self.operandData)
            destination = None
        else:
            destination = self.operandData
            operand = self.getLocationDir(destination)
        return (operand, destination)

    def extended(self):
        operand = "%s" % self.getLocationExt(self.operandData)
        return (operand, self.operandData)

    def relative(self):
        if self.operandData >= 0x80:
            relativeBranchOffset = (0xff & (self.operandData * -1) - 2) * -1
        else:
            relativeBranchOffset = self.operandData + 2
        destination = self.address + relativeBranchOffset
        if relativeBranchOffset == 0:
            operand = "*"
        else:
            operand = "$%04x" % destination
        return (operand, destination)

    def indexed(self):
        return (",X", None)

    def indexedOne(self):
        destination = self.operandData
        operand = "$%02x, X" % destination
        return (operand, destination)

    def indexedTwo(self):
        destination = self.operandData
        operand = "$%04x, X" % destination
        return (operand, destination)

    def processes(self):
        return getattr(self, Operation.METHODS[self.addressingMode])()

    def getLocationExt(self, addr):
        if addr in Operation.symbols:
            return Operation.symbols[addr]
        else:
            return "$%04x" % addr

    def getLocationDir(self, addr):
        if addr in Operation.symbols:
            return Operation.symbols[addr]
        else:
            return "$%02x" % addr


class IllegalOpcode(Exception): pass


class Disassembler(object):
    def __init__(self, opcodes, imageFileName, symbols, indirectAddresses, directAddresses = ()):
        self.opcodes = opcodes
        self.memory = ReadWriteMemory(file(imageFileName, "rb"))
        self.memoryExplorer = MemoryExplorer(size = len(self.memory), offset = 0x0000)
        self.getByte = self.memory.createGetter(1, self.memory.BIG_ENDIAN)
        self.getWord = self.memory.createGetter(2, self.memory.BIG_ENDIAN)
        self.symbols = symbols
        Operation.symbols = self.symbols
        self.pc = 0x0000
        self.callTargets = set(tuple([self.getWord(e) for e in indirectAddresses])).union(set(directAddresses))
        self.jumpTargets = set()
        self.processed = set()
        #print "Call-Targets: ", [hex(x) for x in self.callTargets]
        print sorted([hex(x) for x in self.jumpTargets])

    def disassemble(self):
        lines = set()
        while self.callTargets:
            target = self.callTargets.pop()
            result = self.disassembleTillReturn(target)
            #lines.extend(result)
            lines = lines.union(result)
        #return sorted(set(lines), key = lambda o: o.address)
        return sorted(dict((e.address, e) for e in lines).itervalues(), key = lambda o: o.address)

    def disassembleTillReturn(self, address):
        lines = set()
        origAddress = address
        if address == 0xaf4:
            print ""
        while True:
            try:
                line = self.disassembleLine(address)
            except IndexError as e:
                    print "Index-Error while disassembling line: %s" % e
                    break
            except IllegalOpcode as e:
                    print "Illegal Opcode while disassembling line: %s" % e
                    break
            address += line.size
            #if not self.memoryExplorer.isExplored(origAddress): # and line not in lines:
            if origAddress not in self.processed:
                lines.add(line) #lines.append(line)
            if line.opcode in RETURNS:
                break
        self.processed.add(origAddress)
        while self.jumpTargets:
            target = self.jumpTargets.pop()
            if not self.memoryExplorer.isExplored(target):
                lines = lines.union(self.disassembleTillReturn(target))#lines.extend(self.disassembleTillReturn(target))
        return lines

    def disassembleLine(self, address):
        op = self.getByte(address)
        opcode = self.opcodes[op]
        opcodeName = opcode.name
        addressingMode = opcode.addressingMode
        opcodeSize = opcode.size
        operandData = self.getWord(address + 1) if opcodeSize == 3 else self.getByte(address + 1) if opcodeSize == 2 else None
        operand = ""
        if op in ILLEGAL_OPCODES:
            raise IllegalOpcode("0x%02x [Address: 0x%04x]" % (op, address, ))
        else:
            if address in Operation.symbols:
                #print "0x%04x ==> %s" % (address, Operation.symbols[address])
                label = Operation.symbols[address]
            else:
                label = ''
            operation = Operation(address, opcodeSize, label, op, opcodeName, operand, operandData, addressingMode, '')
            #print "$%04x %02x %s"   % (address, op, operation.formatOperandData()),
            #print opcodeName,

            displayString, destination = operation.processes()
            #print displayString

            self.memoryExplorer.setExplored(address, opcodeSize)
            newAddress = address + opcodeSize
        ##
        ## Code above is almost identical with simulator.
        ##
        ## START SPECIAL.


        ## END SPECIAL.
        ##
        ## Code below is almost identical with simulator.
        ##
        if op in JUMPS:
            if destination and not self.memoryExplorer.isExplored(destination):  # in self.processed:
                self.jumpTargets.add(destination)
        elif op in CALLS:
            if destination and not self.memoryExplorer.isExplored(destination): #destination in self.processed:
                if destination < len(self.memory):       ### CHECK!!!
                    self.callTargets.add(destination)
                else:
                    print "Uups!?"
        return operation


def main():
    #print os.getcwd()

    #mcu = 'HC05BE12'
    #mask = 'BCU20'
    #fileName = r".\knxReTk\imagez\bcu20.bin"

    mcu = 'HC05B6'
    mask = 'BCU12'
    fileName = r".\knxReTk\imagez\bcu12.bin"

    sys.argv.extend([fileName, mcu, mask])

    symbols = Symbols(readConfigData('knxReTk', 'eib.reg'), mcu, mask)

    if len(sys.argv) < 3:
        print "usage: eib_disassemble: file mcu mask"

    if os.access('user.reg', os.F_OK):
        userSymbols = Symbols(open('user.reg').read(), mcu, mask)
        for name, value in userSymbols.sections[(mask, 'labels')]:
            symbols._items[value] = name

    interruptVectors = [v.value for v in symbols.interruptVectors]
    additionalEntries = [s.value for s in symbols.sections[(mask, 'API', )]]

    disassembler = Disassembler(OPCODES, fileName, symbols, interruptVectors, additionalEntries)
    operations = disassembler.disassemble()
    print "=" * 80
    for line in sorted(operations, key = lambda o: o.address):
        print line
    print "=" * 80


if __name__ == '__main__':
    main()

