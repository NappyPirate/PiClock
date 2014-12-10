#this file is designed to be run on a raspberry pi and
#will display a 12 hour clock on a 4 digit 7 segment display
#with 12 pins that are properly connected to GPIO pins

import RPi.GPIO as GPIO
import time
import signal

#this class is designed to represent and control 
#a 4 digit 7 segment display with 12 pins
#specifically one with id# sma420564
class SevenSegmentDisplay:
	#digit displays and the BCM pin numbers they map to 
	d1 = 7
	d2 = 8
	d3 = 3
	d4 = 2

	#BCM pin numbers and the display segments they map to 
	segments = (
		17, #segment a
		18, #segment b
		27, #segment c
		22, #segment d
		23, #segment e
		24, #segment f
		25, #segment g
		4,  #segment p
	)

	#dictionary that maps characters to a 7 bit representation 
	#that maps to the segments needed to display that character, 
	#segments listed in the following order(a, b, c, d, e, f, g)
	characters = {
		"null" : (0,0,0,0,0,0,0),
		"0" : (1,1,1,1,1,1,0),
		"1" : (0,1,1,0,0,0,0),
		"2" : (1,1,0,1,1,0,1),
		"3" : (1,1,1,1,0,0,1),
		"4" : (0,1,1,0,0,1,1),
		"5" : (1,0,1,1,0,1,1),
		"6" : (1,0,1,1,1,1,1),
		"7" : (1,1,1,0,0,0,0),
		"8" : (1,1,1,1,1,1,1),
		"9" : (1,1,1,0,0,1,1)
	}

	#sets up the GPIO pins 
	def __init__(self):
		GPIO.setmode(GPIO.BCM)

		for i in range(len(self.segments)):
			GPIO.setup(self.segments[i], GPIO.OUT)

		GPIO.setup(self.d1, GPIO.OUT)
		GPIO.setup(self.d2, GPIO.OUT)
		GPIO.setup(self.d3, GPIO.OUT)
		GPIO.setup(self.d4, GPIO.OUT)

	#blanks out the current digits then turns off all digits
	def reset_screen(self):
		self.set_digit_character("null", False)
		GPIO.output(self.d1, True)
		GPIO.output(self.d2, True)
		GPIO.output(self.d3, True)
		GPIO.output(self.d4, True)

	#turns on the segments needed to display a character
	#takes a 7 bit list representation for the character
	#and a bool to determine if decimal/colon should be on
	def set_digit_character(self, char, decimal):
		bits = self.characters[char]
		for i in range(len(bits)):
			GPIO.output(self.segments[i], bool(bits[i]))

		GPIO.output(self.segments[7], decimal)

	#grounds a specific digit, making it active
	def set_digit_active(self, digitPin):
		GPIO.output(digitPin, False)


#Callback function to catch POSIX 
#terminate signal and clean up GPIO pins
def signal_term_handler(signal, frame):
	GPIO.cleanup()
	exit(0)

signal.signal(signal.SIGTERM, signal_term_handler)


try:
	display = SevenSegmentDisplay()

	#loop that displays a 12 hour clock on the 4 digit display
	while True:
		currentTime = time.strftime("%I%M")

		display.reset_screen()
		display.set_digit_active(display.d1)
		display.set_digit_character(currentTime[0], False)

		display.reset_screen()
		display.set_digit_active(display.d2)
		display.set_digit_character(currentTime[1], True)

		display.reset_screen()
		display.set_digit_active(display.d3)
		display.set_digit_character(currentTime[2], False)

		display.reset_screen()
		display.set_digit_active(display.d4)
		display.set_digit_character(currentTime[3], False)

except KeyboardInterrupt:
	GPIO.cleanup()
