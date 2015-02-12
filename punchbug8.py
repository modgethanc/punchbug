import RPi.GPIO as GPIO
import time

# Pin Definitons:
pin0 = 4
pin1 = 27
pin2 = 25
pin3 = 24
pin4 = 23
pin5 = 22
pin6 = 18
pin7 = 17

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(pin0, GPIO.IN)
GPIO.setup(pin1, GPIO.IN)
GPIO.setup(pin2, GPIO.IN)
GPIO.setup(pin3, GPIO.IN)
GPIO.setup(pin4, GPIO.IN)
GPIO.setup(pin5, GPIO.IN)
GPIO.setup(pin6, GPIO.IN)
GPIO.setup(pin7, GPIO.IN)

def read():
	val = 0

	if GPIO.input(pin0):
		val += 1
	if GPIO.input(pin1):
		val += 2
	if GPIO.input(pin2):
		val += 4
	if GPIO.input(pin3):
		val += 8
	if GPIO.input(pin4): 
		val += 16
	if GPIO.input(pin5):
		val += 32
	if GPIO.input(pin6):
		val += 64
	if GPIO.input(pin7):
		val += 128
	return val

def render():
	print("reading: %s%s%s%s%s%s%s%s (%s) " + chr(read())) % (GPIO.input(pin0), GPIO.input(pin1), GPIO.input(pin2), GPIO.input(pin3), GPIO.input(pin4), GPIO.input(pin5), GPIO.input(pin6),GPIO.input(pin7), read())

print("starting!\n")
#last = 255
readnext = 0
msg = ''
try:
    while 1:
	#curr = read()
	if read() == 0:	
		readnext = 1
		#last = curr
	if readnext:
		if read() != 0:
			msg += chr(read())
			render()
			readnext = 0
	if read() == 255:
		if msg:
			print msg
			msg = ''

	time.sleep(.1)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
