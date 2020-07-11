import RPi.GPIO as IO

import time          

IO.setwarnings(False)

x=0                  

IO.setmode (IO.BCM)

IO.setup(18,IO.OUT)  

p = IO.PWM(18,100)   
p.start(0)           

while 1:             
   cmd=input("Enyter duty cycle  > ");
   print ("duty= "+str(cmd))
   speed=int(cmd)
   print("Changing to " + str(speed) )
   p.ChangeDutyCycle(speed)
