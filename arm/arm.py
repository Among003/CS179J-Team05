import RPi.GPIO as GPIO
import time
import sys
import os
import math
import threading
import requests

sys.path.insert(0, os.path.abspath("../client"))

import client

hand_motor = [5, 6, 13, 19]
bottom_motor = [12, 16, 20, 21]
motor3 = [4, 17, 27, 22]
motor4 = [24, 25, 8, 7]

DEGREES_PER_STEP = 0.703125
DEGREES_FOR_HAND = 720


GPIO.setmode(GPIO.BCM)
#Hand Motor
GPIO.setup(5, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
#bottom_motor
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
#motor 3
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
#motor 4
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(7, GPIO.OUT)

def moveStepper(in0, in1, in2, in3, motor):
    '''
    Moves stepper motor by one step.
    '''
    GPIO.output(motor[0], in0)
    GPIO.output(motor[1], in1)
    GPIO.output(motor[2], in2)
    GPIO.output(motor[3], in3)
    time.sleep(0.001)

#Each call of foward moves about 0.703125 degrees
def foward(motor):
    '''
    Moves the motor foward(clockwise) by going through each of the 8 steps
    Calls moveStepper function that moves the motor by one step
    '''
    moveStepper(0, 0, 0, 1, motor)
    moveStepper(0, 0, 1, 1, motor)
    moveStepper(0, 0, 1, 0, motor)
    moveStepper(0, 1, 1, 0, motor)
    moveStepper(0, 1, 0, 0, motor)
    moveStepper(1, 1, 0, 0, motor)
    moveStepper(1, 0, 0, 0, motor)
    moveStepper(1, 0, 0, 1, motor)
    moveStepper(0, 0, 0, 0, motor)

def reverse(motor):
    '''
    Moves the motor in reverse(counter-clockwise) by going through each of the 8 steps
    Calls moveStepper function that moves the motor by one step
    '''
    moveStepper(1, 0, 0, 1, motor)
    moveStepper(1, 0, 0, 0, motor)
    moveStepper(1, 1, 0, 0, motor)
    moveStepper(0, 1, 0, 0, motor)
    moveStepper(0, 1, 1, 0, motor)
    moveStepper(0, 0, 1, 0, motor)
    moveStepper(0, 0, 1, 1, motor)
    moveStepper(0, 0, 0, 1, motor)
    moveStepper(0, 0, 0, 0, motor)

def move_cw(degrees, motor):
    '''
    Moves motor in clockwise direction by x degrees. 
    '''
    cnt = int(degrees / DEGREES_PER_STEP)
    for x in range (0, cnt):
        foward(motor)

def move_ccw(degrees, motor):
    '''
    Moves motor in counter-clockwise direction by x degrees. 
    '''
    cnt = int(degrees / DEGREES_PER_STEP)
    for x in range (0, cnt):
        reverse(motor)

def main():
    prev_r = 0
    prev_theta = 0
    prev_z = 0
    prev_hand = False
    while(1):    
        
        data = client.getData()
        x_val = float(data['x'])
        y_val = float(data['y'] )
        z_val = float(data['z'] )
        

  
        hand_val = True if data['hand'] == 'open hand' else False

        #Convert rectangular coordinates to cylindrical
        r_val = math.sqrt(x_val ** 2 + y_val ** 2)
        theta = math.atan(y_val / x_val) * 180 / math.pi  #Angle in degrees

        print(r_val)
        print(theta)
        print(hand_val)

        delta_r = r_val - prev_r
        delta_theta = theta - prev_theta
        delta_z = z_val - prev_z

        if hand_val and not prev_hand:
            t1 = threading.Thread(target= move_ccw,args=(720, hand_motor))
        elif not hand_val and prev_hand:
            t1 = threading.Thread(target= move_cw,args=(720, hand_motor))
        else:
            t1 = threading.Thread(target= move_cw,args=(0, hand_motor))

        if delta_theta >= 0:
            t2 = threading.Thread(target= move_cw,args=(delta_theta * 2, bottom_motor))
        else:
            t2 = threading.Thread(target= move_ccw,args=(delta_theta * 2 * -1, bottom_motor))
        
        if delta_r >= 0:
            t3 = threading.Thread(target= move_cw,args=(delta_r * 360 * 2, motor3))
        else:
            t3 = threading.Thread(target= move_ccw,args=(delta_r * 360 * -1 * 2, motor3))
        
        if delta_z >= 0:
            t4 = threading.Thread(target= move_cw,args=(delta_z * 360 * 2, motor4))
        else:
            t4 = threading.Thread(target= move_ccw,args=(delta_z * 360 * -1 * 2, motor4))
        
        t1.setDaemon(True)
        t2.setDaemon(True)
        t3.setDaemon(True)
        t4.setDaemon(True)
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        '''
        t1 = threading.Thread(target= move_ccw,args=(360, motor1))
        t2 = threading.Thread(target= move_ccw,args=(180, motor2))
        t3 = threading.Thread(target= move_ccw,args=(360, motor3))
        t4 = threading.Thread(target= move_ccw,args=(180, motor4))
        t1.setDaemon(True)
        t2.setDaemon(True)
        t3.setDaemon(True)
        t4.setDaemon(True)
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        t1.join()
        t2.join()
        t3.join()
        t4.join()
        '''

        prev_r = r_val
        prev_theta = theta
        prev_z = z_val
        prev_hand = hand_val

        time.sleep(.1)
    
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #Set all output to 0
        moveStepper(0, 0, 0, 0, hand_motor)
        moveStepper(0, 0, 0, 0, bottom_motor)
        moveStepper(0, 0, 0, 0, motor3)
        moveStepper(0, 0, 0, 0, motor4)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)