from serial import Serial

import sys
import time


# Open Pi serial port, speed 9600 bits per second
serialPort = Serial("/dev/ttyAMA0", 9600)
# Should not need, but just in case

if (serialPort.isOpen() == False):
	serialPort.open()


def blue():
	sys.stdout.write(u"\u001b[46m \u001b[0m")

def grey():
	sys.stdout.write(u"\u001b[47m \u001b[0m") 		

def red():
	sys.stdout.write(u"\u001b[41m \u001b[0m") 												

def startScreen():

	for i in range(0, 24):
    		for j in range(0, 80):	
			nets = [0,1,4,5,8,9,12,13,16,17,20,21]
			
			if (j == 2 or j == 77) and (i >= 11 and i <= 13): 					# paddles
				blue()
			elif (j == 39) and (i in nets): 							# nets
				blue()	
			elif (j == 3) and (i == 12):								# ball
				red()	
			else:											# background
				grey()		

startScreen()

serialPort.close()
	



        

