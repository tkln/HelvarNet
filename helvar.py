#!/usr/bin/python3
import socket
import time
import sys
class HelvarNet:
    DIRECT_LEVEL = '>V:1,C:14,L:{0},F:{1},@{2}#'
    def __init__(self, ip, port):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.connect((ip, port))
    def set_direct_level(self, address, level, fade_time = 0):
        self.__s.send(self.DIRECT_LEVEL.format(level, fade_time, address).encode())

class LedUnit:
    def __init__(self, helvarNet, address):
        self.__net = helvarNet
        self.__addr = address
    def set(self, level, fade_time = 0):
        self.__net.set_direct_level(self.__addr, level, fade_time)
helvarNet = HelvarNet('10.254.1.2', 50000)        
leds = [LedUnit(helvarNet, '1.2.1.1'),
        LedUnit(helvarNet, '1.2.1.2'),
        LedUnit(helvarNet, '1.2.1.3'),
        LedUnit(helvarNet, '1.2.1.4'),
        LedUnit(helvarNet, '1.2.1.5')]
i = 0
while (1):
    leds[i % 5].set(0, 10)
    time.sleep(0.3)
    leds[i % 5].set(10, 10)
    time.sleep(0.3)
    i += 1

#helvarNet.blink()
