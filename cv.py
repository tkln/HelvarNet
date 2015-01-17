#!/usr/bin/python2
import numpy as np
import cv2
import helvar
import time

helvarNet = helvar.HelvarNet('10.254.1.2', 50000)        
leds = [helvar.LedUnit(helvarNet, '1.2.1.1'),
        helvar.LedUnit(helvarNet, '1.2.1.2'),
        helvar.LedUnit(helvarNet, '1.2.1.3'),
        helvar.LedUnit(helvarNet, '1.2.1.4'),
        helvar.LedUnit(helvarNet, '1.2.1.5')]

def leds_off():
    for led in leds:
        led.set(0, 0)

cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
prev_frame = None


def find_contours(image):
    contours, _ = cv2.findContours(cont_frame, cv2.RETR_LIST, 
                                   cv2.CHAIN_APPROX_SIMPLE)
    return contours

def center(rect):
    return [rect[0] + rect[2] / 2, rect[1] + rect[3] / 2]

while(True):
    ret, frame = cap.read()

    gray = cv2.medianBlur(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), 17)

    if (prev_frame == None):
        prev_frame = gray
    movement_frame = 1 - (cv2.add(-gray, prev_frame))
    _, bin_frame = cv2.threshold(movement_frame, 10, 50, cv2.THRESH_BINARY)
    prev_frame = gray
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cont_frame = bin_frame.copy()
    conts = find_contours(cont_frame)
    segments = {}
    for c in conts:
        rect = cv2.boundingRect(c)
        if cv2.contourArea(c) > 100:
            cv2.rectangle(movement_frame, (rect[0], rect[1]), 
                          (rect[0] + rect[2], rect[1] + rect[3]), (255, 0, 0))
            """print(rect)
            print(5 * center(rect)[0] / movement_frame.shape[1])
            leds[5 * center(rect)[0] / movement_frame.shape[1]].set(50, 100)"""
            segments[5 * center(rect)[0] / movement_frame.shape[1]] = True
    time.sleep(0.05)
    leds_off()
    for segment in segments:
        leds[segment].set(50, 100)
    cv2.drawContours(movement_frame, conts, -1, (255, 255, 0), 1)
    cv2.imshow('frame', movement_frame)
    
cap.release()
cv2.destroyAllWindows()
