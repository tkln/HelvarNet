#!/usr/bin/python3
import socket
import time
HELVARNET_PORT = 50000
HELVARNET_IP = '10.254.1.2'
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HELVARNET_IP, HELVARNET_PORT))
time.sleep(1)
#s.send('>V:2,C:11,G:100,B:2,S:1,F:200#'.encode('ASCII')) #toimii
while (1):
    s.send('>V:1,C:14,L:0,F:30,@1.2.1.1#'.encode('ASCII')) #toimii
    time.sleep(0.5)
    s.send('>V:1,C:14,L:10,F:30,@1.2.1.1#'.encode('ASCII')) #toimii
    time.sleep(0.5)
#data = s.recv(128).decode()
#print(data)
