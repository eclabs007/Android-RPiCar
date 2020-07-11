#Libraries
import RPi.GPIO as GPIO
import time
import sys,select 
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 23
GPIO_ECHO = 24
GPIO_FWD = 18 
GPIO_BKWD = 4
GPIO_LFT=3
GPIO_RGT=2
GPIO_LED =25
FREQ=100
speed=0
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_FWD, GPIO.OUT)
pwm0=GPIO.PWM(GPIO_FWD,FREQ)
GPIO.setup(GPIO_BKWD, GPIO.OUT)
GPIO.setup(GPIO_LFT, GPIO.OUT)
GPIO.setup(GPIO_RGT, GPIO.OUT)
GPIO.setup(GPIO_LED, GPIO.OUT)

GPIO.setup(GPIO_ECHO, GPIO.IN)
 
GPIO.output(GPIO_LED, False)
GPIO.output(GPIO_BKWD, False)
#GPIO.output(GPIO_FWD, False)
pwm0.start(0)
is_fwd=0
safe_distance=True
def stop():
    GPIO.output(GPIO_BKWD, False)
    #GPIO.output(GPIO_FWD, False)
    GPIO.output(GPIO_LFT, False)
    GPIO.output(GPIO_RGT, False)
    GPIO.output(GPIO_LED, False)
    pwm0.ChangeDutyCycle(0)
def fwd(duty):
    is_fwd=1
    if safe_distance == False:
        return
#    GPIO.output(GPIO_BKWD, False)
#    GPIO.output(GPIO_FWD, True)
    pwm0.ChangeDutyCycle(duty)
    GPIO.output(GPIO_LED, True)
    time.sleep(0.2)
    stop()


def bkwd():
    GPIO.output(GPIO_BKWD, True)
    GPIO.output(GPIO_FWD, False)
    time.sleep(0.2)
    stop()

def right():

    pwm0.ChangeDutyCycle(100)
    GPIO.output(GPIO_LFT, False)
    GPIO.output(GPIO_RGT, True)
    time.sleep(0.2)
    stop()
def left():

    pwm0.ChangeDutyCycle(100)
    GPIO.output(GPIO_LFT, True)
    GPIO.output(GPIO_RGT, False)
    time.sleep(0.2)
    stop()
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
import socket
UDP_IP = "0.0.0.0"
UDP_PORT = 8888

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


i=1
if __name__ == '__main__':
    try:
        while True:
            
            if i :

                cmd, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
  #              cmd=sys.stdin.readline().strip()
                print "cmd ",cmd
                if cmd == 'f':
                    fwd(100)
                elif cmd == 'b':
                    bkwd()
                elif cmd == 'r':
                    right()
                elif cmd == 'l':
                    left()
                elif cmd== 's':
                    stop()
                elif cmd== '1':
                    speed=35
                    fwd(speed)
                elif cmd== '2':
                    speed=55
                    fwd(speed)
                elif cmd== '3':
                    speed=70
                    fwd(speed)
                elif cmd== '4':
                    speed=85
                    fwd(speed)

                cmd=0
            print("Speed= "+str(speed))
            dist = distance()
            if dist<70 or  dist > 400:
               safe_distance=False;
               stop()
               GPIO.output(GPIO_LED, False)
               if is_fwd == 1 :
                  bkwd()
                  is_fwd=0
        
               print (" Stop ")
            else:
                safe_distance=True;
               
            print ("Measured Distance = %.1f cm" % dist)
          #  time.sleep(0.1)
 	    
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

