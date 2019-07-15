# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 20:07:45 2016

@author: Christophe
"""

import socket
import binascii
import socket
import struct
import sys

HOST = '127.0.0.1'
PORT = 5000


values = (1, 'ab', 2.7)
packer = struct.Struct('I 2s f')
packed_data = packer.pack(*values)

# 1) Creation du socket
mySocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

print >>sys.stderr, 'sending "%s"' % binascii.hexlify(packed_data), values
mySocket.sendto(packed_data,(HOST,PORT))