#to control the servo

import RPi.GPIO as GPIO  
import time  
import sys


def move(angle, timer):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.OUT)
	pwm=GPIO.PWM(17, 50)
	pwm.start(5)
	GPIO.output(17, True)
	time.sleep(0.1)
	duty = 1/18*(int(angle))+2
	while(timer > 0):
		pwm.ChangeDutyCycle(duty)
		timer = timer - 1
		time.sleep(0.001)
	time.sleep(2)
	pwm.stop()
	GPIO.cleanup()



move(sys.argv[1], 100)
now = time.ctime()
print(now)

#move(60, 100)



