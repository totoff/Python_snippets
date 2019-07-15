# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 19:28:16 2016

@author: Christophe
"""

import socket, sys

HOST = '127.0.0.1'
PORT = 5000

# 1) Creation du socket
mySocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

mySocket.sendto("Salut",(HOST,PORT))