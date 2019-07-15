# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 18:24:09 2016

@author: Christophe
"""

import socket, sys

HOST = '127.0.0.1'
PORT = 5000

# 1) Creation du socket
mySocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# 2) bind du socket
try:
    mySocket.bind((HOST,PORT))
except socket.error:
    print "bind du socket Impossible"
    sys.exit()
    print "Fin"

while 1:
    # 3) Attente de requete de connexion client
    print "Serveur pret => En attente de requetes"
    mySocket.listen(5)
    
    # Etablissement de la connexion
    connexion, adresse=mySocket.accept()
    print "Client connecte, adresse IP %s, port %s" % (adresse[0], adresse[1])
    
    # Dialogue avec le client
    connexion.send("Vous etes connecte au serveur Marcel")
    msgClient = connexion.recv(1024)
    
    while 1:
        print "C>", msgClient
        if msgClient.upper() == "FIN" or msgClient == "":
            break
        msgServeur = raw_input("S> ")
        connexion.send(msgServeur)
        msgClient = connexion.recv(1024)
    
    #Fernmeture de la connexion
    connexion.send("Au revoir!")
    connexion.close()
    
    ch = raw_input("<R>ecommencer <T>erminer ?")
    if ch.upper() == 'T' :
        break
