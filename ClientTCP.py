# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 18:33:16 2016

@author: Christophe
"""

import socket, sys

HOST = '127.0.0.1'
PORT = 5000

# 1) Creation du socket
mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    mySocket.connect((HOST,PORT))
except socket.error :
    print "Echec de la connexion"
    sys.exit()
    
msgServeur = mySocket.recv(1024)

while 1:
    if msgServeur.upper() == "FIN" or msgServeur == "":
        break
    print "S>", msgServeur
    msgClient = raw_input("C>")
    mySocket.send(msgClient)
    msgServeur = mySocket.recv(1024)

mySocket.close()
    