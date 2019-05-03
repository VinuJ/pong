import RPi.GPIO as GPIO
import time

DEBOUNCE_TIME = 0.3
SAMPLE_FREQUENCY = 10
MAXIMUM = (DEBOUNCE_TIME * SAMPLE_FREQUENCY)

integrator = 0	

class d_bounce:
	def __init__(self, pin):
		self.pin = pin

		GPIO.setwarnings(False) 	
        	GPIO.setmode(GPIO.BCM) 	

       	 	GPIO.setup(self.pin, GPIO.IN)
		
    	def output_state( self ):
		global integrator
		global MAXIMUM
		output = 0 

        	if (GPIO.input(self.pin) == 0):
            		if(integrator > 0):
                		integrator -= 1
        	elif(integrator < MAXIMUM):
            		integrator += 1

        	if(integrator == 0):
            		output = 0
        	elif(integrator >= MAXIMUM):
            		output = 1
            		integrator = MAXIMUM

        	return output
	
		

def main():
	print("main program")
	button = d_bounce( 11 )

    	while True:
		if(button.output_state() == 1):
			print("OFF")
		else:
			print("ON")
		time.sleep(0.1)


if __name__ == '__main__':
	try:
        	main()
  	except KeyboardInterrupt:
        	GPIO.cleanup()
