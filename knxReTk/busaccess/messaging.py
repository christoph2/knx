#!/usr/bin/env python
# -*- coding: utf-8 -*-


import array

def createByteBuffer(size):
    arr = array.array('B')
    arr.fromlist([0] * size)
    return arr

class MessageBuffer(object):
    pass

class MessageSystem(object):
    pass

def main():
    pass

if __name__ == '__main__':
    main()
