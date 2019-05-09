import RPi.GPIO as GPIO
import time

class h_bounce:
	def __init__(self, pin):
		self.pin = pin

		GPIO.setwarnings(False) 	
        	GPIO.setmode(GPIO.BCM) 	

       	 	GPIO.setup(self.pin, GPIO.IN)
		
    	def output_state( self ):
		state = GPIO.input(self.pin)
        	return state

button = h_bounce (11)

while True:
	if(button.output_state() == 1):
		print("ON")
	else:
		print("OFF")
	time.sleep(0.1)
