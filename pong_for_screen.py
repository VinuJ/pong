from serial import Serial
import sys
import math
import RPi.GPIO as GPIO
import smbus
import time

# Open Pi serial port, speed 9600 bits per second
serialPort = Serial("/dev/ttyAMA0", 115200)
# Should not need, but just in case

if (serialPort.isOpen() == False):
	serialPort.open()

# Colours

def blue():
	serialPort.write(u"\u001b[46m \u001b[0m") 
	

def grey():
	serialPort.write(u"\u001b[47m \u001b[0m") 		
	

def red():
	serialPort.write(u"\u001b[41m \u001b[0m")
	

# Cursor Navigation	

def c_up(steps):
	for i in range(0, steps):
		serialPort.write(u"\u001b[1A")
		
def c_down(steps):
	for i in range(0, steps):
		serialPort.write(u"\u001b[1B")
		
def c_right(steps):
	for i in range(0, steps):
		serialPort.write(u"\u001b[1C")
		
def c_left(steps):
	for i in range(0, steps):
		serialPort.write(u"\u001b[1D")
		
# Shift Cursor And Fill

def shiftAndFill(shiftx, shifty, colour):
	c_right(shiftx)
	c_up(shifty)
	colour()
	c_left(shiftx+1)
	c_down(shifty)
	
# Starting Screen

def startScreen():

	for i in range(0, 24):
    		for j in range(0, 80):	
			nets = [0,1,4,5,8,9,12,13,16,17,20,21]
			
		 	if (j == 39) and (i in nets): # nets
				blue()		
			else: # background
				grey()		
				
playerServe = 2 # which player is serving

# ADC Classes

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

class h_bounce:
	def __init__(self, pin):
		self.pin = pin

		GPIO.setwarnings(False) 	
        	GPIO.setmode(GPIO.BCM) 	

       	 	GPIO.setup(self.pin, GPIO.IN)
		
    	def output_state( self ):
		state = GPIO.input(self.pin)
        	return state

# ADC Functions

def superPad1():

	button = h_bounce (11)

	if (button.output_state() == 1):
		return 1
	else:
		return 0

def superPad2():

	button = h_bounce (11)

	if (button.output_state() == 1):
		return 1
	else:
		return 0


def countADC1(superp):
	
	I2CADDR = 0x21 
	CMD_CODE = 0x10

	bus = smbus.SMBus(1) 

	bus.write_byte( I2CADDR, CMD_CODE ) 
	tmp = bus.read_word_data( I2CADDR, 0x00 ) 

	tmp = ( ( ( (tmp << 8) + (tmp >> 8) ) | 0xFFF000 ) ^ 0xFFF000 )

	tmp = math.floor(tmp / 155)
	
	if (superp == 1):
		if (tmp <= 2):
			countModified = 2
		elif (tmp >= 21):
			countModified = 21
		else:
			countModified = tmp
	else:
		if (tmp <= 1):
			countModified = 1
		elif (tmp >= 22):
			countModified = 22
		else:
			countModified = tmp
				
	countModified = int(countModified)

	return countModified

def countADC2(superp):
	v_resistor1 = v_resistor( 9, 10 )

	    
	countA = v_resistor1.update()
	
	if (superp == 1):
		if (countA <= 2):
			countModified = 2
		elif (countA >= 21):
			countModified = 21
		else:
			countModified = countA
	else:
		if (countA <= 1):
			countModified = 1
		elif (countA >= 22):
			countModified = 22
		else:
			countModified = countA		

	return countModified

# Ball Class

class Ball:
	
	def __init__ (self, oldx, oldy, newx, newy):
		self.oldx = oldx
		self.oldy = oldy
		self.newx = newx
		self.newy = newy
		
		if (playerServe == 2):
			self.xdirection = -1
		else:
			self.xdirection = 1	
	
		self.ydirection = 1

	def drawBall (self, oldx, oldy, newx, newy):
		nets = [2,3,6,7,10,11,14,15,18,19,22,23]
		
		if (oldx == 39) and (oldy in nets):
			shiftAndFill(self.oldx, self.oldy, blue)
		else:
			shiftAndFill(self.oldx, self.oldy, grey)	
				   
		shiftAndFill(self.newx, self.newy, red)
	
	def updateBallPos (self, oldx, oldy, newx, newy):
		self.oldx = self.newx
		self.oldy = self.newy
	
		self.newx = self.oldx + self.xdirection
		self.newy = self.oldy + self.ydirection

		if (self.newx == 3) or (self.newx == 76):
			self.xdirection = -self.xdirection

		if (self.newy == 0) or (self.newy == 23):
			self.ydirection = -self.ydirection

# Paddle Class

class Paddle:
	def __init__ (self, x, oldy, newy):
		self.x = x
		self.oldy = oldy
		self.newy = newy

	def drawPaddle (self, x, oldy, newy, superp):
		if (self.newy == self.oldy) and (self.oldy != 11):
			self.newy = self.oldy	
		else:
			if (superp == 1):
				for i in range(4):
					shiftAndFill(self.x, self.oldy-2+i, grey)
				for j in range(4):
					shiftAndFill(self.x, self.newy-2+j, blue)
			else:
				for i in range(2):
					shiftAndFill(self.x, self.oldy-1+i, grey)
				for j in range(2):
					shiftAndFill(self.x, self.newy-1+j, blue)


def runGame():
			
	startScreen()

	c_left(80) # move to (0, 0)

	if (playerServe == 1):
		ball = Ball(3, 11, 3, 11)
	
	if (playerServe == 2):
		ball = Ball(76, 11, 76, 11)

	paddle1 = Paddle(2, 11, 11)
	paddle2 = Paddle(77, 11, 11) 


	while(True):

		# Paddle

		paddle1.drawPaddle(paddle1.x, paddle1.oldy, paddle1.newy, superPad1())
		paddle2.drawPaddle(paddle2.x, paddle2.oldy, paddle2.newy, superPad2())
		
		paddle1.oldy = paddle1.newy
		paddle2.oldy = paddle2.newy

		paddle1.newy = 	countADC1(superPad1())
		paddle2.newy = 	countADC2(superPad2())

		# Ball

		ball.drawBall(ball.oldx, ball.oldy, ball.newx, ball.newy)

		ball.updateBallPos(ball.oldx, ball.oldy, ball.newx, ball.newy)
		
	
		time.sleep(0.05)



runGame()

serialPort.close()

GPIO.cleanup()
