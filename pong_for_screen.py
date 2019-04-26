from serial import Serial

import sys
import time


# Open Pi serial port, speed 9600 bits per second
serialPort = Serial("/dev/ttyAMA0", 9600)
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
		

# Starting Screen

def startScreen():

	for i in range(0, 24):
    		for j in range(0, 80):	
			nets = [0,1,4,5,8,9,12,13,16,17,20,21]
			
			if (j == 2 or j == 77) and (i >= 11 and i <= 13): # paddles
				blue()
			elif (j == 39) and (i in nets): # nets
				blue()	
			elif (j == 3) and (i == 12): # ball
				red()	
			else: # background
				grey()		

startScreen()

time.sleep(1)

c_up(12)
c_right(4)

def ball_move_dleft():
	c_left(1)
	grey()
	c_down(1)
	red()

ball_move_dleft()

serialPort.close()

	



        

