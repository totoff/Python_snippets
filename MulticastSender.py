# -*- coding: utf-8 -*-
"""
Created on Thu Sep 01 20:14:47 2016

@author: Christophe
"""

import socket
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

while 1:
	sock.sendto("robot", (MCAST_GRP, MCAST_PORT))
	time.sleep(1)