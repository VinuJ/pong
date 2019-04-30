import RPi.GPIO as GPIO				
import time

class v_resistor():
    def __init__( self, pinI, pinO  ):
        self.count = 0
        self.RESET_PIN = pinO
        self.TEST_PIN = pinI

        GPIO.setwarnings(False) 	
        GPIO.setmode(GPIO.BCM) 		

        GPIO.setup(self.RESET_PIN, GPIO.OUT) 
        GPIO.output(self.RESET_PIN, False) 	

        GPIO.setup(self.TEST_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update( self ):
	self.count = 0
        GPIO.output(self.RESET_PIN, True) 	
        time.sleep(0.001)
        GPIO.output(self.RESET_PIN, False) 

        while GPIO.input(self.TEST_PIN) == 0:
             self.count +=1		

        return self.count 

    def getCount( self ):
        return self.count

# Main program block

def main():
    print("main program")
    v_resistor1 = v_resistor( 9, 10 )

    while True: 
        countA = v_resistor1.update()

        outputString = "Count = " + str(countA) 
        print outputString
	
        time.sleep(1) 		
    

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
