import RPi.GPIO as GPIO
import time

from arm import move_cw, move_ccw, moveStepper

hand_motor = [5, 6, 13, 19]
bottom_motor = [12, 16, 20, 21]
motor3 = [4, 17, 27, 22]
motor4 = [24, 25, 8, 7]

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

def main():
    #Test hand fully opens then fully closes
    move_ccw(720, hand_motor)
    move_cw(720, hand_motor)

    #Test arm rotation. Rotates by 180 degrees
    move_cw(180, hand_motor)
    move_ccw(180, hand_motor)

    #Test vertical movement
    move_cw(50, motor4)
    time.sleep(.5)
    move_ccw(50, motor4)
    time.sleep(.5)
    move_cw(10, motor4)

    GPIO.cleanup()




if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        #Set all output to 0
        moveStepper(0, 0, 0, 0, hand_motor)
        moveStepper(0, 0, 0, 0, bottom_motor)
        moveStepper(0, 0, 0, 0, motor3)
        moveStepper(0, 0, 0, 0, motor4)
        GPIO.cleanup()
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
