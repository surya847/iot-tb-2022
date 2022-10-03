import time
import RPi.GPIO as GPIO       ## Import GPIO library
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)      ## Use board pin numbering
GPIO.setup(3, GPIO.OUT)      ## Setup GPIO Pin 11 to OUT
while True:
	GPIO.output(3,True)  ## Turn on Led
	time.sleep(1)         ## Wait for one second
	GPIO.output(3,False) ## Turn off Led
	time.sleep(1)         ## Wait for one second
