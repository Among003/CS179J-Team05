import RPi.GPIO as GPIO
import time

PIN0 = 5
PIN1 = 6
PIN2 = 13
PIN3 = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN0, GPIO.OUT)
GPIO.setup(PIN1, GPIO.OUT)
GPIO.setup(PIN2, GPIO.OUT)
GPIO.setup(PIN3, GPIO.OUT)

def moveStepper(in0, in1, in2, in3):
    GPIO.output(PIN0, in0)
    GPIO.output(PIN1, in1)
    GPIO.output(PIN2, in2)
    GPIO.output(PIN3, in3)
    time.sleep(0.007)

#Each call of foward moves about 0.703125 degrees
def foward():
    moveStepper(0, 0, 0, 1)
    moveStepper(0, 0, 1, 1)
    moveStepper(0, 0, 1, 0)
    moveStepper(0, 1, 1, 0)
    moveStepper(0, 1, 0, 0)
    moveStepper(1, 1, 0, 0)
    moveStepper(1, 0, 0, 0)
    moveStepper(1, 0, 0, 1)

def reverse():
    moveStepper(1, 0, 0, 1)
    moveStepper(1, 0, 0, 0)
    moveStepper(1, 1, 0, 0)
    moveStepper(0, 1, 0, 0)
    moveStepper(0, 1, 1, 0)
    moveStepper(0, 0, 1, 0)
    moveStepper(0, 0, 1, 1)
    moveStepper(0, 0, 0, 1)


while(1):
    for x in range(0, 512):
        foward()
    time.sleep(1)
    for x in range(0, 512):
        reverse()