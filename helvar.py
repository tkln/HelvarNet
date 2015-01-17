#!/usr/bin/python3
import socket
import time
import sys
import threading
import weakref

class HelvarNet:
    DIRECT_LEVEL = '>V:1,C:14,L:{0},F:{1},@{2}#'
    def __init__(self, ip, port):
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.connect((ip, port))
        self.__t = threading.Thread(target = self.__t_func, args = (self, weakref.ref(self)))
        self.__lock = threading.RLock()
        self.__running = True
        self.__t.start()
    def set_direct_level(self, address, level, fade_time = 0):
        self.__send(self.DIRECT_LEVEL.format(level, fade_time, address))
    def __send(self, str):
        self.__lock.acquire()
        self.__s.send(str.encode())
        self.__lock.release()
    def __keepalive(self):
        self.__send('')
    def __t_func(self, weakself, _):
        while (self.__running):
            time.sleep(1)
            if weakself() is None:
                break
            self.__keepalive()
    def __exit__(self):
        self.__running = False

class LedUnit:
    def __init__(self, helvarNet, address):
        self.__net = helvarNet
        self.__addr = address
    def set(self, level, fade_time = 0):
        self.__net.set_direct_level(self.__addr, level, fade_time)

if __name__ == "__main__":
    #helvarNet = HelvarNet('10.254.1.2', 50000)        
    leds = []
    with HelvarNet('10.254.1.2', 50000) as helvarNet:
        leds = [LedUnit(helvarNet, '1.2.1.1'),
                LedUnit(helvarNet, '1.2.1.2'),
                LedUnit(helvarNet, '1.2.1.3'),
                LedUnit(helvarNet, '1.2.1.4'),
                LedUnit(helvarNet, '1.2.1.5')]
    i = 0
    while (1):
        for i in range(5):
            leds[i].set(50, 100)
            time.sleep(0.5)
        for i in range(5):
            leds[i].set(0, 100)
            time.sleep(0.5)
            i += 1
