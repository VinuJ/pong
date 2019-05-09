from serial import Serial

import sys

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
			
		#	if (j == 2 or j == 77) and (i >= 11 and i <= 13): # paddles
		#		blue()
		 	if (j == 39) and (i in nets): # nets
				blue()		
			else: # background
				grey()		
				
playerServe = 2 # which player is serving

superpaddle = 0 # superpaddle


# ADC 2 Class

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


# ADC 2 Input Function

def count():
	v_resistor1 = v_resistor( 9, 10 )

	    
	countA = v_resistor1.update()
	

	if (countA <= 1):
		countModified = 1
	elif (countA >= 22):
		countModified = 22
	else:
		countModified = countA

	outputString = "Count = " + str(countModified) 

	print outputString
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

	def drawPaddle (self, x, oldy, newy, superpaddle):
		if (newy == oldy) and (oldy != 11):
			newy = oldy	
		else:

			if (superpaddle == 1):
				superpaddle == 1
			else:
				shiftAndFill(self.x, self.oldy - 1, grey)
				shiftAndFill(self.x, self.oldy, grey)
				shiftAndFill(self.x, self.oldy + 1, grey)
	
				shiftAndFill(self.x, self.newy - 1, blue)
				shiftAndFill(self.x, self.newy, blue)
				shiftAndFill(self.x, self.newy + 1, blue)


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

		paddle1.drawPaddle(paddle1.x, paddle1.oldy, paddle1.newy, superpaddle)
		paddle2.drawPaddle(paddle2.x, paddle2.oldy, paddle2.newy, superpaddle)
	
		ball.drawBall(ball.oldx, ball.oldy, ball.newx, ball.newy)

		ball.updateBallPos(ball.oldx, ball.oldy, ball.newx, ball.newy)
		
		paddle1.oldy = paddle1.newy
		paddle2.oldy = paddle2.newy

		paddle1.newy = 	count()
		paddle2.newy = 	count()
	
		time.sleep(0.05)



runGame()

serialPort.close()
GPIO.cleanup()

