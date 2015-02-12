#!/usr/bin/python
import twitter
import RPi.GPIO as GPIO
import time

# twitter setup
configfile = open("twitconfig.txt", "r")

ck = configfile.readline().rstrip('\r\n')
cs = configfile.readline().rstrip('\r\n')
atk = configfile.readline().rstrip('\r\n')
ats = configfile.readline().rstrip('\r\n')

twit = twitter.Api(consumer_key=ck,
                      consumer_secret=cs,
                      access_token_key=atk,
                      access_token_secret=ats)

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
	print("%s%s%s%s%s%s%s%s (%s) " + chr(read())) % (GPIO.input(pin0), GPIO.input(pin1), GPIO.input(pin2), GPIO.input(pin3), GPIO.input(pin4), GPIO.input(pin5), GPIO.input(pin6),GPIO.input(pin7), read())


#===== MAIN 

if twit.VerifyCredentials():
	print "twitter login successful!"

print("reading!\n")
readnext = 0
msg = ''
try:
    while 1:
	if read() == 0:	
		readnext = 1
	if readnext and read() !=0:
		render()
		readnext = 0
		if read() > 31 and read() < 127:
			msg += chr(read())
	if read() == 255 and msg:
		twit.PostUpdate(msg)
		print "tweeting: " + msg
		msg = ''

	time.sleep(.5)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.cleanup() # cleanup all GPIO
