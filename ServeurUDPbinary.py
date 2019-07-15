# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 18:24:09 2016

@author: Christophe
"""

import binascii
import socket
import struct
import sys

HOST = '127.0.0.1'
PORT = 5000

unpacker = struct.Struct('I 2s f')

# 1) Creation du socket
mySocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

# 2) bind du socket
try:
    mySocket.bind((HOST,PORT))
except socket.error:
    print "bind du socket Impossible"
    sys.exit()
    print "Fin"

while 1:
    # 3) Attente de requete de connexion client
    print "Serveur pret => Attente de messages UDP"
    data, adresse = mySocket.recvfrom(1024)
    
    print >>sys.stderr, 'received "%s"' % binascii.hexlify(data)
    unpacked_data = unpacker.unpack(data)
    print >>sys.stderr, 'unpacked:', unpacked_data

mySocket.close()