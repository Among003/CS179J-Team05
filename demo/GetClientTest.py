import os
import requests as req
import json
import sys
import time
import RPi.GPIO as GPIO

url = "http://ec2-54-153-87-218.us-west-1.compute.amazonaws.com/"

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)


while(1):
    data = 0
    r = req.get(url + "/getData/",  headers={'Cache-Control': 'no-cache'})

    if r.ok:
        data = r.json()
        xVal = int(data['x'])
        yVal = int(data['y'])
        handVal = bool(data['hand'])
        print("x: " + str(xVal) + " y: " + str(yVal) + " hand: " + str(handVal))
    r.close()

    if(xVal > 0):
        GPIO.output(16, GPIO.HIGH)
    else:
        GPIO.output(16, GPIO.LOW)
    
    if(yVal > 0):
        GPIO.output(20, GPIO.HIGH)
    else:
        GPIO.output(20, GPIO.LOW)
    if(handVal):
        GPIO.output(21, GPIO.HIGH)
    else:
        GPIO.output(21, GPIO.LOW)
    
    time.sleep(1)






