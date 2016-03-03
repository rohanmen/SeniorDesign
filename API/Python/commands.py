import RPi.GPIO as GPIO ## Import GPIO library
import time
import mcp3008

#how to use pwm
#https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

#stuff on callbacks
#http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/


#define all pins here
LED = 7
#servo goes to GPIO 18
SPICLK = 23
SPIMISO = 21
SPIMOSI = 19
SPICS = 22

#linear actuator pins
LIN1 = 35
LIN2 = 37

LOW_VAL = 0
PULL_OUT = 1
 


#***************************************************************
#******servo control functions**********************************
def set(property, value):
	try:
		f = open("/sys/class/rpi-pwm/pwm0/" + property, 'w')
		f.write(value)
		f.close()	
	except:
		print("Error writing to: " + property + " value: " + value)
 
 
def setServo(angle):
	set("servo", str(angle))

#***************************************************************
#***************************************************************


def setup():
	GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
	#GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
	GPIO.setup(LED, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
	#GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(LIN1, GPIO.OUT)
	GPIO.setup(LIN2, GPIO.OUT)
	#add setup code here

	# set up the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)


	#servo setup
	set("delayed", "0")			#turn the delay mode off
	set("mode", "servo")		#set the mode to be 'servo'
	set("servo_max", "180")		#set the maximum servo value
	set("active", "1")			#make the output pin active


def turnOn(pin):
	GPIO.output(pin,True)

def turnOff(pin):
	GPIO.output(pin,False)

def wait(seconds):
	time.sleep(seconds)


#ir distance sensor code
#takes 3.3V
def get_ir_distance(channel):
	r = []
	for i in range(0, 10):
	    r.append(mcp3008.readadc(channel))
    	a = sum(r)/10.0
    	v = (a/1023.0)*3.3

    	#calibrate using this formulta
    	d = 16.2537 * v**4 - 129.893 * v**3 + 382.268 * v**2 - 512.611 * v + 306.439
    	cm = int(round(d))
	return cm


#servo control example
#http://blog.enthought.com/general/raspberry-pi-sensor-and-actuator-control/#.VsdW9JMrLVo
#only GPIO 18 for servo
#more reference
#https://learn.adafruit.com/adafruits-raspberry-pi-lesson-8-using-a-servo-motor/software
def move_servo(start_angle, end_angle):
	delay_period = 0.01

	if (start_angle <= end_angle):
		for angle in range(start_angle, end_angle):
			setServo(angle)
			time.sleep(delay_period)
	else:
		for angle in range(end_angle, start_angle):
			setServo(start_angle - angle)
			time.sleep(delay_period)



# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
        if ((adcnum > 7) or (adcnum < 0)):
                return -1
        GPIO.output(cspin, True)
 
        GPIO.output(clockpin, False)  # start clock low
        GPIO.output(cspin, False)     # bring CS low
 
        commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
                if (commandout & 0x80):
                        GPIO.output(mosipin, True)
                else:
                        GPIO.output(mosipin, False)
                commandout <<= 1
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
 
        adcout = 0
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(clockpin, True)
                GPIO.output(clockpin, False)
                adcout <<= 1
                if (GPIO.input(misopin)):
                        adcout |= 0x1
 
        GPIO.output(cspin, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
        return adcout

def extend_lin_actuator():
	print "extend"
	turnOn(LIN1)
	turnOff(LIN2)
	#set bits

def retract_lin_actuator():
	print "retract"
	turnOn(LIN2)
	turnOff(LIN1)
	#set bits

def stop_lin_actuator():
	print "stop"
	turnOff(LIN1)
	turnOff(LIN2)
	#set bits

def pull_to_zero():
	print "zero"
	retract_lin_actuator()
	i=0
	while (readadc(0,SPICLK,SPIMOSI,SPIMISO,SPICS) > distance):
		i++
	stop_lin_actuator()


def pull_psu(distance):
	print distance
	i = 0;
	extend_lin_actuator()
	while (readadc(0,SPICLK,SPIMOSI,SPIMISO,SPICS) < distance):
		i++

	wait(5)

	retract_lin_actuator()
	while (readadc(0,SPICLK,SPIMOSI,SPIMISO,SPICS) > PULL_OUT):
		i++

	stop_lin_actuator()
	wait(5)


