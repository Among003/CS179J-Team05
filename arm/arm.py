import RPi.GPIO as GPIO
import time
import sys
import os
import math
import threading
import requests

PIN0 = 5
PIN1 = 6
PIN2 = 13
PIN3 = 19

motor1 = [5, 6, 13, 19]
motor2 = [12, 16, 20, 21]

DEGREES_PER_STEP = 0.703125

GPIO.setmode(GPIO.BCM)
#motor 1
GPIO.setup(PIN0, GPIO.OUT)
GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)
GPIO.setup(PIN3, GPIO.OUT)
#motor 2
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

def moveStepper(in0, in1, in2, in3, motor):
    GPIO.output(motor[0], in0)
    GPIO.output(motor[1], in1)
    GPIO.output(motor[2], in2)
    GPIO.output(motor[3], in3)
    time.sleep(0.001)

#Each call of foward moves about 0.703125 degrees
def foward(motor):
    moveStepper(0, 0, 0, 1, motor)
    moveStepper(0, 0, 1, 1, motor)
    moveStepper(0, 0, 1, 0, motor)
    moveStepper(0, 1, 1, 0, motor)
    moveStepper(0, 1, 0, 0, motor)
    moveStepper(1, 1, 0, 0, motor)
    moveStepper(1, 0, 0, 0, motor)
    moveStepper(1, 0, 0, 1, motor)

def reverse(motor):
    moveStepper(1, 0, 0, 1, motor)
    moveStepper(1, 0, 0, 0, motor)
    moveStepper(1, 1, 0, 0, motor)
    moveStepper(0, 1, 0, 0, motor)
    moveStepper(0, 1, 1, 0, motor)
    moveStepper(0, 0, 1, 0, motor)
    moveStepper(0, 0, 1, 1, motor)
    moveStepper(0, 0, 0, 1, motor)

def move_cw(degrees, motor):
    cnt = int(degrees / DEGREES_PER_STEP)
    for x in range (0, cnt):
        foward(motor)

def move_ccw(degrees, motor):
    cnt = int(degrees / DEGREES_PER_STEP)
    for x in range (0, cnt):
        reverse(motor)

def main():
    while(1):    
        t1 = threading.Thread(target= move_cw,args=(360, motor1))
        t2 = threading.Thread(target= move_cw,args=(180, motor2))
        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        t1 = threading.Thread(target= move_ccw,args=(360, motor1))
        t2 = threading.Thread(target= move_ccw,args=(180, motor2))
        t1.setDaemon(True)
        t2.setDaemon(True)
        t1.start()
        t2.start()

        t1.join()
        t2.join()

        time.sleep(2)


        #move_cw(360, motor1)
        #move_ccw(360, motor1)
        #move_cw(180, motor2)
        #move_ccw(180, motor2)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #Set all output to 0
        moveStepper(0, 0, 0, 0, motor1)
        moveStepper(0, 0, 0, 0, motor2)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)