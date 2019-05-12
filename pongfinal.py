# VERSION WITH SCORE
# REMOVED FOR LOOP
# BALL DOESN'T DELETE SCORE

from serial import Serial
import sys
import math
import RPi.GPIO as GPIO
import smbus
import time

e = chr(27)

# SCORE NUMBERS


l_no0x = [29,29,29,29,29,30,30,31,31,31,31,31] 
r_no0x = [47,47,47,47,47,48,48,49,49,49,49,49] 
no0y = [22,21,20,19,18,22,18,22,21,20,19,18] 


l_no1x = [29,29,30,30,30,30,30,31]
r_no1x = [47,47,48,48,48,48,48,49]
no1y = [21,28,22,21,20,19,18,18]

l_no2x = [29,29,29,29,30,30,30,31,31,31,31]
r_no2x = [47,47,47,47,48,48,48,49,49,49,49] 
no2y = [22,20,19,18,22,20,18,22,21,20,18]

l_no3x = [29,29,29,30,30,30,31,31,31,31,31]
r_no3x = [47,47,47,48,48,48,49,49,49,49,49]
no3y = [22,20,18,22,20,18,22,21,20,19,18]

l_no4x = [29,29,29,30,31,31,31,31,31]
r_no4x = [47,47,47,48,49,49,49,49,49] 
no4y = [22,21,20,20,22,21,20,19,18]

l_no5x = [31,30,29,29,29,30,31,31,31,30,29]
r_no5x = [49,48,47,47,47,48,49,49,49,48,47]
no5y = [22,22,22,21,20,20,20,19,18,18,18]

l_no6x = [31,30,29,29,29,30,31,31,31,30,29,29]
r_no6x = [49,48,47,47,47,48,49,49,49,48,47,47] 
no6y = [22,22,22,21,20,20,20,19,18,18,18,19]

l_no7x = [31,30,29,31,30,30,30]
r_no7x = [49,48,47,49,48,48,48] 
no7y = [22,22,22,21,20,19,18]

l_no8x = [31,30,29,31,29,31,30,29,31,29,31,30,29]
r_no8x = [49,48,47,49,47,49,48,47,49,47,49,48,47] 
no8y = [22,22,22,21,21,20,20,20,19,19,18,18,18]

l_no9x = [29,29,29,29,30,30,30,31,31,31,31,31]
r_no9x = [47,47,47,47,48,48,48,49,49,49,49,49] 
no9y = [22,21,20,18,22,20,18,22,21,20,19,18]

# Open Pi serial port, speed 9600 bits per second
serialPort = Serial("/dev/ttyAMA0", 115200)
# Should not need, but just in case

if (serialPort.isOpen() == False):
	serialPort.open()

# Colours

def blue():
	serialPort.write(u"\u001b[46m \u001b[0m") 
	

def black():
	serialPort.write(u"\u001b[30m \u001b[0m") 		
	

def red():
	serialPort.write(u"\u001b[41m \u001b[0m")

def magenta():
	serialPort.write(u"\u001b[35m \u001b[0m")
	

# Cursor Navigation	

def c_up(steps):
	steps = str(steps)
	serialPort.write(u"\u001b["+steps+"A")
		
def c_down(steps):
	steps = str(steps)
	serialPort.write(u"\u001b["+steps+"B")
		
def c_right(steps):
	steps = str(steps)
	serialPort.write(u"\u001b["+steps+"C")
		
def c_left(steps):
	steps = str(steps)
	serialPort.write(u"\u001b["+steps+"D")
		
# Shift Cursor And Fill

def shiftAndFill(shiftx, shifty, colour):
	c_right(shiftx)
	c_up(shifty)
	colour()
	c_left(shiftx+1)
	c_down(shifty)
	
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

	button = h_bounce (18)

	if (button.output_state() == 1):
		return 1
	else:
		return 0

def superPad2():

	button = h_bounce (17)

	if (button.output_state() == 1):
		return 1
	else:
		return 0

def serve1():

	button = h_bounce (11)

	if (button.output_state() == 1):
		return 0
	else:
		return 1
def serve2():

	button = h_bounce (4)

	if (button.output_state() == 1):
		return 1
	else:
		return 0

def countADC1(superp): # very little noise
	
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

def countADC2(superp): # lots of noise
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

		# If statements so that the ball can go over the score without deleting it
		
		if player1.newscore == 0:
			for i in range(len(l_no0x)):
				if (oldx == l_no0x[i] and oldy == no0y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 1:
			for i in range(len(l_no1x)):
				if (oldx == l_no1x[i] and oldy == no1y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 2:
			for i in range(len(l_no2x)):
				if (oldx == l_no2x[i] and oldy == no2y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 3:
			for i in range(len(l_no3x)):
				if (oldx == l_no3x[i] and oldy == no3y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 4:
			for i in range(len(l_no4x)):
				if (oldx == l_no4x[i] and oldy == no4y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 5:
			for i in range(len(l_no5x)):
				if (oldx == l_no5x[i] and oldy == no5y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 6:
			for i in range(len(l_no6x)):
				if (oldx == l_no6x[i] and oldy == no6y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 7:
			for i in range(len(l_no7x)):
				if (oldx == l_no7x[i] and oldy == no7y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player1.newscore == 8:
			for i in range(len(l_no8x)):
				if (oldx == l_no8x[i] and oldy == no8y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)			

		if player1.newscore == 9:
			for i in range(len(l_no9x)):
				if (oldx == l_no9x[i] and oldy == no9y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)
	
		if player2.newscore == 0:
			for i in range(len(r_no0x)):
				if (oldx == r_no0x[i] and oldy == no0y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 1:
			for i in range(len(r_no1x)):
				if (oldx == r_no1x[i] and oldy == no1y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 2:
			for i in range(len(r_no2x)):
				if (oldx == r_no2x[i] and oldy == no2y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 3:
			for i in range(len(r_no3x)):
				if (oldx == r_no3x[i] and oldy == no3y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 4:
			for i in range(len(r_no4x)):
				if (oldx == r_no4x[i] and oldy == no4y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 5:
			for i in range(len(r_no5x)):
				if (oldx == r_no5x[i] and oldy == no5y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 6:
			for i in range(len(r_no6x)):
				if (oldx == r_no6x[i] and oldy == no6y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 7:
			for i in range(len(r_no7x)):
				if (oldx == r_no7x[i] and oldy == no7y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		if player2.newscore == 8:
			for i in range(len(r_no8x)):
				if (oldx == r_no8x[i] and oldy == no8y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)			

		if player2.newscore == 9:
			for i in range(len(r_no9x)):
				if (oldx == r_no9x[i] and oldy == no9y[i]):
					shiftAndFill(self.oldx, self.oldy, magenta)

		# If statement so that the ball can go over the net withotu deleting it
		
		if (oldx == 39) and (oldy in nets):
			shiftAndFill(self.oldx, self.oldy, blue)
		else: # Else just fill oldx and oldy with black, the background colour
			shiftAndFill(self.oldx, self.oldy, black)


				   
		shiftAndFill(self.newx, self.newy, red) # Fill new ball position red
	
	def updateBallPos (self, oldx, oldy, newx, newy):
		self.oldx = self.newx
		self.oldy = self.newy
	
		self.newx = self.oldx + self.xdirection
		self.newy = self.oldy + self.ydirection

		if (self.newx == 3) or (self.newx == 76): # If the ball hits horizontal limits, reverse direction
			self.xdirection = -self.xdirection

		if (self.newy == 0) or (self.newy == 23): # If the ball hits vertical limits, reverse direction
			self.ydirection = -self.ydirection

	def hitPaddle (self, oldx, oldy, paddley, superp):	
				if (superp == 1): # Checking if the paddle is 5 wide
					if (self.oldx == 3) or (self.oldx == 76): # If on the line just before the paddle
						if (paddley-2 <= self.oldy <= paddley+2): # If ball's y pos is within the paddle's y pos
							return 1
						else:
							return 0			
				else: # Same thing for 3 wide paddle
					if (self.oldx == 3) or (self.oldx == 76): 
						if (paddley-1 <= self.oldy <= paddley+1):
							return 1
						else:
							return 0
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
				for i in range(5):
					shiftAndFill(self.x, self.oldy-2+i, black)
				for j in range(5):
					shiftAndFill(self.x, self.newy-2+j, blue)
			else:
				for i in range(3):
					shiftAndFill(self.x, self.oldy-1+i, black)
				for j in range(3):
					shiftAndFill(self.x, self.newy-1+j, blue)

# Player Class

class Player:
		def __init__ (self, oldscore, newscore):
			self.oldscore = oldscore
			self.newscore = newscore 

# Score Functions

def scoreFill(number, player, colour):

	# 0

	if (number == 0) and (player == 1) :
		for i in range(len(l_no0x)):
			shiftAndFill(l_no0x[i], no0y[i], colour)

	if (number == 0) and (player == 2) :
		for i in range(len(r_no0x)):
			shiftAndFill(r_no0x[i], no0y[i], colour)
	
	# 1

	if (number == 1) and (player == 1) :
		for i in range(len(l_no1x)):
			shiftAndFill(l_no1x[i], no1y[i], colour)

	if (number == 1) and (player == 2) :
		for i in range(len(r_no1x)):
			shiftAndFill(r_no1x[i], no1y[i], colour)

	# 2

	if (number == 2) and (player == 1) :
		for i in range(len(l_no2x)):
			shiftAndFill(l_no2x[i], no2y[i], colour)

	if (number == 2) and (player == 2) :
		for i in range(len(r_no2x)):
			shiftAndFill(r_no2x[i], no2y[i], colour)

	# 3

	if (number == 3) and (player == 1) :
		for i in range(len(l_no3x)):
			shiftAndFill(l_no3x[i], no3y[i], colour)

	if (number == 3) and (player == 2) :
		for i in range(len(r_no3x)):
			shiftAndFill(r_no3x[i], no3y[i], colour)

	# 4

	if (number == 4) and (player == 1) :
		for i in range(len(l_no4x)):
			shiftAndFill(l_no4x[i], no4y[i], colour)

	if (number == 4) and (player == 2) :
		for i in range(len(r_no4x)):
			shiftAndFill(r_no4x[i], no4y[i], colour)

	# 5

	if (number == 5) and (player == 1) :
		for i in range(len(l_no5x)):
			shiftAndFill(l_no5x[i], no5y[i], colour)

	if (number == 5) and (player == 2) :
		for i in range(len(r_no5x)):
			shiftAndFill(r_no5x[i], no5y[i], colour)

	# 6

	if (number == 6) and (player == 1) :
		for i in range(len(l_no6x)):
			shiftAndFill(l_no6x[i], no6y[i], colour)

	if (number == 6) and (player == 2) :
		for i in range(len(r_no6x)):
			shiftAndFill(r_no6x[i], no6y[i], colour)

	# 7

	if (number == 7) and (player == 1) :
		for i in range(len(l_no7x)):
			shiftAndFill(l_no7x[i], no7y[i], colour)

	if (number == 7) and (player == 2) :
		for i in range(len(r_no7x)):
			shiftAndFill(r_no7x[i], no7y[i], colour)

	# 8

	if (number == 8) and (player == 1) :
		for i in range(len(l_no8x)):
			shiftAndFill(l_no8x[i], no8y[i], colour)

	if (number == 8) and (player == 2) :
		for i in range(len(r_no8x)):
			shiftAndFill(r_no8x[i], no8y[i], colour)

	# 9

	if (number == 9) and (player == 1) :
		for i in range(len(l_no9x)):
			shiftAndFill(l_no9x[i], no9y[i], colour)

	if (number == 9) and (player == 2) :
		for i in range(len(r_no9x)):
			shiftAndFill(r_no9x[i], no9y[i], colour)

# Starting Screen

def startScreen():

	for i in range(0, 24):
    		for j in range(0, 80):	
			nets = [0,1,4,5,8,9,12,13,16,17,20,21]
			
		 	if (j == 39) and (i in nets): # nets
				blue()		
			else: # background
				black()	

	c_left(80) # move to (0, 0)	

	# Set score to 0 - 0

	player1 = Player(0, 0) 
	player2 = Player(0, 0)

startScreen()


def runRound():

	counter1 = 0
	
	
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
		
		if (ball.oldx == 4) or (ball.oldx == 75):
			counter1+=1
		
		if (counter1 > 1):			
			if (ball.hitPaddle(ball.oldx, ball.oldy, paddle1.oldy, superPad1()) == 0):
				print("player 1 missed")
				shiftAndFill(ball.oldx, ball.oldy, black)
				GPIO.output(leds[tempx], False)

				player2.oldscore = player2.newscore
				player2.newscore = player2.oldscore + 1

				break
				
			elif (ball.hitPaddle(ball.oldx, ball.oldy, paddle1.oldy, superPad1()) == 1):
				print("player 1 hit")
				
							
			elif (ball.hitPaddle(ball.oldx, ball.oldy, paddle2.oldy, superPad2()) == 0):
				print("player 2 missed")	
				shiftAndFill(ball.oldx, ball.oldy, black)
				GPIO.output(leds[tempx], False)
				
				player1.oldscore = player1.newscore
				player1.newscore = player1.oldscore + 1

				break
							
			elif (ball.hitPaddle(ball.oldx, ball.oldy, paddle2.oldy, superPad2()) == 1):
				print("player 2 hit")
		
		# Lights

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		GPIO.setup((10, 5, 6, 12, 13, 16, 19, 20, 26), GPIO.OUT)

		leds = (5, 6, 12, 13, 16, 19, 20, 26)
		
		tempx = ball.oldx
		tempx = tempx - 2
		tempx = float(tempx) / 9.125

		if (tempx >= 8):
			tempx = 8
		else:
			tempx = math.ceil(tempx)

		tempx = tempx - 1
		tempx = int(tempx)
		
		# Now tempx is value from 0-7

		if (ball.xdirection == -1) and (tempx < 7):
			GPIO.output(leds[tempx+1], False)

		elif (ball.xdirection == 1) and (tempx > 0):
			GPIO.output(leds[tempx-1], False)

		GPIO.output(leds[tempx], True)



paddle1 = Paddle(2, 11, 11)
paddle2 = Paddle(77, 11, 11) 

scoredrawn = 0

while (True): # Game Loop
	
	if player1.newscore == 10:
		print("Player 1 Wins!")
		break
	if player2.newscore == 10:
		print("Player 2 Wins!")
		break

	if scoredrawn == 0:	
		scoreFill(player1.oldscore, 1, black)
		scoreFill(player2.oldscore, 2, black)
			
		scoreFill(player1.newscore, 1, magenta)
		scoreFill(player2.newscore, 2, magenta)

		scoredrawn = 1

	paddle1.drawPaddle(paddle1.x, paddle1.oldy, paddle1.newy, superPad1())
	paddle2.drawPaddle(paddle2.x, paddle2.oldy, paddle2.newy, superPad2())
		
	paddle1.oldy = paddle1.newy
	paddle2.oldy = paddle2.newy

	paddle1.newy = 	countADC1(superPad1())
	paddle2.newy = 	countADC2(superPad2())

	if (serve1() == 1):
		scoredrawn = 0
		playerServe = 1
		ball = Ball(3, paddle1.oldy, 3, paddle1.oldy)
		runRound()
	
	if (serve2() == 1):
		scoredrawn = 0
		playerServe = 2
		ball = Ball(76, paddle2.oldy, 76, paddle2.oldy)
 		runRound()

serialPort.close()

GPIO.cleanup()
