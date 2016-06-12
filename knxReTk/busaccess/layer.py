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


import array
from collections import namedtuple
import struct
import threading
import Queue

from knxReTk.utilz import bytes
from knxReTk.utilz.classes import SingletonBase, RepresentationMixIn
from knxReTk.utilz.threads import Thread

MAX_QUEUE_SIZE = 2

MSG_LEN_STD         = 22
MAX_ADPU_LEN_STD    = 14
MAX_PROP_DATA_LEN   = 10

NO_ROUTING_CTRL     = 7
HOP_COUNT           = 6

# Addr: 0061 Addr: 1152

def wordToBytes(w):
    h, l = struct.pack(">H", w)
    return (ord(h), ord(l), )

"""
typedef uint8_t Knx_MessageType[MSG_LEN];

typedef struct tagKnxMsg_Buffer {
    uint8_t next;
    uint8_t len;
    Knx_ServiceTypeType service;
    uint8_t sap;
    Knx_StatusType status;
    Knx_MessageType msg;
} KnxMsg_Buffer, * KnxMsg_BufferPtr;

typedef struct tagKNX_StandardFrameType {
    uint8_t   ctrl;
    uint8_t   source[2];
    uint8_t   dest[2];
    uint8_t   npci;
    uint8_t   tpci;
    uint8_t   apci;
    uint8_t   data[MAX_ADPU_LEN];
} KNX_StandardFrameType, * KNX_StandardFrameRefType;    /* KNX_StandardFrameType */

typedef struct tagKNX_PropertyFrameType {
    uint8_t   ctrl;
    uint8_t   source[2];
    uint8_t   dest[2];
    uint8_t   npci;
    uint8_t   tpci;
    uint8_t   apci;
    uint8_t   obj_id;
    uint8_t   prop_id;
    uint8_t   num_elems;
    uint8_t   start_index;
    uint8_t   data[MAX_PROP_DATA_LEN];
} KNX_PropertyFrameType, * KNX_PropertyFrameRefType;    /* KNX_PropertyFrameType */

typedef struct tagKNX_PollingFrameType {
    uint8_t   ctrl;
    uint8_t   source[2];
    uint8_t   poll_addr[2];
    uint8_t   num_slots;
    uint8_t   slot[MAX_ADPU_LEN];
} KNX_PollingFrameType, * KNX_PollingFrameRefType;  /* KNX_PollingFrameType */

"""


class StandardFrame(RepresentationMixIn):
    DAF_MULTICAST       = 0x80
    DAF_INDIVIDUAL      = 0x00

    def __init__(self, frame):
        self._frame = frame

    @property
    def ctrl(self):
        return self._frame[0]

    @ctrl.setter
    def ctrl(self, value):
        self._frame[0] = bytes.loByte(value)

    @property
    def source(self):
        return bytes.makeWord(self._frame[1], self._frame[2])

    @source.setter
    def source(self, value):
        h, l = wordToBytes(value)
        self._frame[1] = h
        self._frame[2] = l

    @property
    def dest(self):
        return bytes.makeWord(self._frame[3], self._frame[4])

    @dest.setter
    def dest(self, value):
        h, l = wordToBytes(value)
        self._frame[3] = h
        self._frame[4] = l

    @property
    def npci(self):
        return self._frame[5]

    @npci.setter
    def npci(self, value):
        self._frame[5] = bytes.loByte(value)

    @property
    def tpci(self):
        return self._frame[6]

    @tpci.setter
    def tpci(self, value):
        self._frame[6] = bytes.loByte(value)

    @property
    def apci(self):
        return  (self.tpci << 8) | self._frame[7]

    @apci.setter
    def apci(self, value):
        h, l = wordToBytes(value)
        self.tpci |= h
        self._frame[7] = l

    @property
    def data(self):
        return self._frame[8 : ]

    @data.setter
    def data(self, value):
        self._frame[8 : ] = value

    @property
    def frameType(self):
        return self.ctrl & 0xc0

    @frameType.setter
    def frameType(self, value):
        self.ctrl |= (value & 0xc0) | 0x30

    @property
    def priority(self):
        return (self.ctrl & 0x0c) >> 2

    @priority.setter
    def priority(self, value):
        self.ctrl |= ((value & 0x03) << 2)

    @property
    def addressType(self):
        return self.npci & 0x80

    @addressType.setter
    def addressType(self, value):
        self.npci |= (value & 0x80)

    @property
    def isMulticastAddressed(self):
        return self.addressType == StandardFrame.DAF_MULTICAST

    @property
    def isIndividualAddressed(self):
        return self.addressType == StandardFrame.DAF_INDIVIDUAL

    @property
    def lsduLen(self):
        return self.npci & 0x0f

    @lsduLen.setter
    def lsduLen(self, value):
        self.npci |= (value & 0x0f)

    @property
    def seqNo(self):
        return (self.tpci & 0x3c) >> 2

    @seqNo.setter
    def seqNo(self, value):
        self.tpci |= ((value & 0x0f) << 2)

    def setRoutingCount(self):
        if (self.ctrl & 0x02) == 0x02:
            hopCount = NO_ROUTING_CTRL
            self.ctrl &= 0x02
        else:
            hopCount = HOP_COUNT
        self.npci |= ((hopCount & 0x07) << 4)


class MessageBuffer(RepresentationMixIn):

    def __init__(self, initial = None):
        if initial is None:
            initial = []
        self._msg = MessageBuffer.createBuffer(MSG_LEN_STD, initial)
        self._length = len(initial)
        self._service = None
        self._status = None
        self._confirmation = None

    @staticmethod
    def createBuffer(size, initial):
        arr = array.array('B', initial)
        if len(arr) < size:
            arr.extend([0] * (size - len(arr)))
        return arr

    def copy(self):
        return MessageBuffer(self._msg)

    def asStandardFrame(self):
        return StandardFrame(self._msg)

    def asList(self):
        return self._msg[ : self._length]

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, value):
        self._service = bytes.loByte(value)

    @property
    def status(self):
        return self._status

    @service.setter
    def status(self, value):
        self._status = bytes.loByte(value)

    @property
    def confirmed(self):
        return self._confirmation

    @confirmed.setter
    def confirmed(self, value):
        self._confirmation = value

ServiceGroup = namedtuple('ServiceGroup', 'instance services')

class ServiceError(Exception):
    pass


class DispatcherThread(Thread):

    def __init__(self, layer):
        super(DispatcherThread, self).__init__()
        self.layer = layer

    def execute(self):
        try:
            message = self.layer.queue.get(block = False)
        except Queue.Empty as e:
            pass
        else:
            if message:
                serviceHandler = self.layer.SERVICES.get(message.service)
                if serviceHandler is None:
                    raise ServiceError("Invalid Service Code: 0x{0:02x}".format(message.service))
                serviceHandler(self.layer, message)
                self.layer.queue.task_done()


class Layer(SingletonBase):

    serviceRegistry = {}

    def __init__(self):
        Layer.serviceRegistry[self.SERVICE_GROUP] = ServiceGroup(self, self.SERVICES)
        self.queue = Queue.Queue(maxsize = MAX_QUEUE_SIZE)
        self.initialize()
        self.dispatcher = DispatcherThread(self)
        self.dispatcher.start()

    def post(self, message):
        if message.service is None:
            raise ServiceError("Missing Service Code.")
        else:
            serviceGroup = message.service & 0xf0
            if serviceGroup not in Layer.serviceRegistry:
                raise ServiceError("Service Group unknwon: 0x{0:02x}".format(serviceGroup))
            instance, services = Layer.serviceRegistry.get(serviceGroup)
            instance.queue.put(message, block = True)

    def initialize(self):
        pass

    def dispatch(self, message):
        pass


"""/*
** Global variables.
*/
KnxMsg_BufferPtr KnxMsg_ScratchBufferPtr;

#if KSTACK_MEMORY_MAPPING == STD_ON
    #define KSTACK_START_SEC_CODE
    #include "MemMap.h"
#endif /* KSTACK_MEMORY_MAPPING */

/*
** Global functions.
*/
#if KSTACK_MEMORY_MAPPING == STD_ON
FUNC(void, KSTACK_CODE) KnxDisp_DispatchLayer(const uint8_t LayerID,
                                              CONSTP2CONST(Knx_LayerServicesType, AUTOMATIC, KSTACK_APPL_DATA) ServiceTable
                                              );
#else
void KnxDisp_DispatchLayer(const uint8_t LayerID, const Knx_LayerServicesType * ServiceTable)
#endif /* KSTACK_MEMORY_MAPPING */
{
    uint8_t entry;

    do {
        KnxMsg_ScratchBufferPtr = KnxMsg_Get(LayerID);

        if (KnxMsg_ScratchBufferPtr != (KnxMsg_BufferPtr)NULL) {
            entry = KnxMsg_ScratchBufferPtr->service - ServiceTable->LayerOffset;

            if (entry < ServiceTable->NumServices) {
                /* todo: _ASSERT() Function-Pointer!=NULL !!! */
                ServiceTable->Functions[entry]();
            } else {
                KnxMsg_ReleaseBuffer(KnxMsg_ScratchBufferPtr);
            }
        }
    } while (KnxMsg_ScratchBufferPtr != (KnxMsg_BufferPtr)NULL);
}


#if KSTACK_MEMORY_MAPPING == STD_ON
    #define KSTACK_STOP_SEC_CODE
    #include "MemMap.h"
#endif /* KSTACK_MEMORY_MAPPING */
"""
