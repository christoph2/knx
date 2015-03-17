#!/usr/bin/env python
# -*- coding: utf-8 -*-


##
##  System Interface Objects.
##

OBJECT_TYPES = {
    0:  "DEVICE_OBJECT",
    1:  "ADDRESSTABLE_OBJECT",
    2:  "ASSOCIATIONTABLE_OBJECT",
    3:  "APPLICATIONPROGRAM_OBJECT",
    4:  "INTERFACEPROGRAM_OBJECT",
    10: "POLLING_MASTER",
}


##
## Interface Object Type independent Standardized Property Identifiers.
##
PROPERTY_IDENTIFIERS = {
    1:  "PID_OBJECT_TYPE",
    2:  "PID_OBJECT_NAME",
    3:  "PID_SEMAPHOR",
    4:  "PID_GROUP_OBJECT_REFERENCE",
    5:  "PID_LOAD_STATE_CONTROL",
    6:  "PID_RUN_STATE_CONTROL",
    7:  "PID_TABLE_REFERENCE",
    8:  "PID_SERVICE_CONTROL",
    9:  "PID_FIRMWARE_REVISION",
    10: "PID_SERVICES_SUPPORTED",
    11: "PID_SERIAL_NUMBER",
    12: "PID_MANUFACTURER_ID",
    13: "PID_PROGRAM_VERSION",
    14: "PID_DEVICE_CONTROL",
    15: "PID_ORDER_INFO",
    16: "PID_PEI_TYPE",
    17: "PID_PORT_CONFIGURATION",
    18: "PID_POLL_GROUP_SETTINGS",
    19: "PID_MANUFACTURER_DATA",
    20: "PID_ENABLE",
    21: "PID_DESCRIPTION",
    22: "PID_FILE",
    23: "PID_GROUP_ADDRESS_LIST",

##
## Interface Object Type specific Standardized Property Identifiers.
##
    51: "PID_POLLING_STATE",
    52: "PID_POLLING_SLAVE_ADDR",
    53: "PID_POLL_CYCLE",

## Extension:
    0xfe: "PID_SYSTEM_OBJECT_EXTENSION",
}



##
##  Property Data Types Identifiers.
##
PROPERTY_DATA_TYPES = {
    0x00:   "PDT_CONTROL",
    0x01:   "PDT_CHAR",
    0x02:   "PDT_UNSIGNED_CHAR",
    0x03:   "PDT_INT",
    0x04:   "PDT_UNSIGNED_INT",
    0x05:   "PDT_KNX_FLOAT",
    0x06:   "PDT_DATE",
    0x07:   "PDT_TIME",
    0x08:   "PDT_LONG",
    0x09:   "PDT_UNSIGNED_LONG",
    0x0A:   "PDT_FLOAT",
    0x0B:   "PDT_DOUBLE",
    0x0C:   "PDT_CHAR_BLOCK",
    0x0D:   "PDT_POLL_GROUP_SETTINGS",
    0x0E:   "PDT_SHORT_CHAR_BLOCK",

    0x11:   "PDT_GENERIC_01",
    0x12:   "PDT_GENERIC_02",
    0x13:   "PDT_GENERIC_03",
    0x14:   "PDT_GENERIC_04",
    0x15:   "PDT_GENERIC_05",
    0x16:   "PDT_GENERIC_06",
    0x17:   "PDT_GENERIC_07",
    0x18:   "PDT_GENERIC_08",
    0x19:   "PDT_GENERIC_09",
    0x1A:   "PDT_GENERIC_10",

    # following from 'BIM_M13x.h:
    0x1B:   "PDT_GENERIC_11",
    0x1C:   "PDT_GENERIC_12",
    0x1D:   "PDT_GENERIC_13",
    0x1E:   "PDT_GENERIC_14",
    0x1F:   "PDT_GENERIC_15",
    0x20:   "PDT_GENERIC_16",
    0x21:   "PDT_GENERIC_17",
    0x22:   "PDT_GENERIC_18",
    0x23:   "PDT_GENERIC_19",
    0x24:   "PDT_GENERIC_20",
    0x30:   "PDT_VERSION",
    0x31:   "PDT_ALARM_INFO",
    0x32:   "PDT_BINARY_INFORMATION",
    0x33:   "PDT_BITSET8",
    0x34:   "PDT_BITSET16",
    0x35:   "PDT_ENUM8",
    0x36:   "PDT_SCALING",
    0x3E:   "PDT_FUNCTION",
    0x54:   "PDT_SERVICE_CONTROL",     ## UNDOCUMENTED, BUT OBSERVED (BCU2).
    0x5b:   "PDT_DEVICE_CONTROL",
}


def objectType(value):
    result = OBJECT_TYPES.get(value, '')
    return "%s[%u]" % (result, value)

def propertyIdentifier(value):
    result = PROPERTY_IDENTIFIERS.get(value, '')
    return "%s[%u]" % (result, value)

def propertyDataType(value):
    result = PROPERTY_DATA_TYPES.get(value, '')
    return "%s[%u]" % (result, value)

