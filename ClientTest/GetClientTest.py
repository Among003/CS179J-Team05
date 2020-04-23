import os
import requests as req
import json
import sys
import time
#import RPi.GPIO as GPIO

url = "http://ec2-54-153-87-218.us-west-1.compute.amazonaws.com/"

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
    
    time.sleep(1)






