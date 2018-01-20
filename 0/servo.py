#to control the servo

import RPi.GPIO as GPIO  
import time  
import sys



def move(angle):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(17, GPIO.OUT)
	pwm=GPIO.PWM(17, 50)
	pwm.start(5)	
	GPIO.output(17, True)
	time.sleep(0.1)
	duty = 1/18*(int(angle))+2
	pwm.ChangeDutyCycle(duty)
	time.sleep(2)
	pwm.stop()
	GPIO.cleanup()


if __name__=="__main__":
	move(sys.argv[1])
	#move(0)



