from serial import Serial

import sys
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

# Ball Functions

def drawBall(oldx, oldy, newx, newy):
	
	if (oldx == 39) and (oldy in 
	shiftAndFill(oldx, oldy, grey)
	
	shiftAndFill(newx, newy, red)

def forward():
	ball.newx += 1

def backward():
	ball.newx -= 1	
		
# Starting Screen

def startScreen():

	for i in range(0, 24):
    		for j in range(0, 80):	
			nets = [0,1,4,5,8,9,12,13,16,17,20,21]
			
			if (j == 2 or j == 77) and (i >= 11 and i <= 13): # paddles
				blue()
		 	elif (j == 39) and (i in nets): # nets
				blue()		
			else: # background
				grey()		
				
# Ball Class

class Ball:
	
	def __init__ (self, oldx, oldy, newx, newy):
		self.oldx = oldx
		self.oldy = oldy
		self.newx = newx
		self.newy = newy

		self.xdirection = 1	
		self.ydirection = 1

	def drawBall (self, oldx, oldy, newx, newy):
	
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

def runGame():
			
	startScreen()

	c_left(80) # move to (0, 0)

	playerServe = 1 # which player is serving

	if (playerServe == 1):
		ball = Ball(3, 11, 3, 11)
	
	if (playerServe == 2):
		ball = Ball(77, 11, 77, 11)


	while(True):
	
		ball.drawBall(ball.oldx, ball.oldy, ball.newx, ball.newy)

		ball.updateBallPos(ball.oldx, ball.oldy, ball.newx, ball.newy)
	
		time.sleep(0.05)
		
runGame()

serialPort.close()
