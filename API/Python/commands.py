import RPi.GPIO as GPIO ## Import GPIO library
import time

#how to use pwm
#https://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/

#stuff on callbacks
#http://makezine.com/projects/tutorial-raspberry-pi-gpio-pins-and-python/

#GLOBALS
MAX_DISTANCE_LIN = 0
MIN_DISTANCE_LIN = 100
MAX_DISTANCE_TRACK = 700
MIN_DISTANCE_TRACK = 100
PULL_OUT = 50
CURRENT_LEVEL = 0

#define all pins here
LED = 7
#servo goes to GPIO 18
#orange
SPICLK = 23
#yellow
SPIMISO = 21
#blue
SPIMOSI = 19
#violet
SPICS = 22

#linear actuator pins
LIN1 = 35
LIN2 = 37

#track actuator pins
TRK1 = 36
TRK2 = 38

#vertical track actuator pins
RGT_TRK1 = 3
RGT_TRK2 = 5
LFT_TRK1 = 11
LFT_TRK2 = 13


#ADC Channels
LIN_CHN = 0
TRK_CHN = 1
VER_CHN = 2
CUR_CHN = 3

#BUTTONS
#Calibrate Button
C_BUTTON = 40
#Vertical Level Limit Switches
LEVEL0 = 29
LEVEL1 = 31
LEVELS = [LEVEL0, LEVEL1]
 


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


#***************************************************************
#******initialize the GPIO Pins*********************************
def setup():
	GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
	#GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
	GPIO.setup(LED, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
	#GPIO.setup(C_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(C_BUTTON, GPIO.IN)	#calibrate button
	GPIO.setup(LIN1, GPIO.OUT)		#lin actuator
	GPIO.setup(LIN2, GPIO.OUT)
	GPIO.setup(TRK1, GPIO.OUT)		#track actuator
	GPIO.setup(TRK2, GPIO.OUT)
	GPIO.setup(RGT_TRK1, GPIO.OUT)	#vertical
	GPIO.setup(RGT_TRK2, GPIO.OUT)
	GPIO.setup(LFT_TRK1, GPIO.OUT)
	GPIO.setup(LFT_TRK1, GPIO.OUT)
	GPIO.setup(LEVEL0, GPIO.IN)		#limit switches
	GPIO.setup(LEVEL1, GPIO.IN)

	#add setup code here

	#add setup for vertical actuators and limit switches

	# set up the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)


	#servo setup
	#set("delayed", "0")			#turn the delay mode off
	#set("mode", "servo")		#set the mode to be 'servo'
	#set("servo_max", "180")		#set the maximum servo value
	#set("active", "1")			#make the output pin active
	time.sleep(0.5)
#***************************************************************
#***************************************************************


def cleanup():
	GPIO.cleanup()


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
	    #r.append(mcp3008.readadc(channel))
	    r.append(1)
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


#***************************************************************
#*******FUNCTIONS TO CONTROL ACTUATORS**************************
#***************************************************************
#***************************************************************
def get_lin_feedback():
	return readadc(LIN_CHN,SPICLK,SPIMOSI,SPIMISO,SPICS)

def get_track_feedback():
	return readadc(TRK_CHN,SPICLK,SPIMOSI,SPIMISO,SPICS)

def get_vertical_feedback():
	return readadc(VER_CHN,SPICLK,SPIMOSI,SPIMISO,SPICS)

def get_current_feedback():
	return readadc(CUR_CHN,SPICLK,SPIMOSI,SPIMISO,SPICS)

def extend_lin_actuator():
	print "extend lin actuator"
	turnOn(LIN1)
	turnOff(LIN2)

def extend_track_actuator():
	print "extend track actuator"
	turnOn(TRK1)
	turnOff(TRK2)

def retract_lin_actuator():
	print "retractlin actuator"
	turnOn(LIN2)
	turnOff(LIN1)

def retract_track_actuator():
	print "retract track actuator"
	turnOn(TRK2)
	turnOff(TRK1)

def stop_lin_actuator():
	print "stop lin actuator"
	turnOn(LIN1)
	turnOn(LIN2)

def stop_track_actuator():
	print "stop track actuator"
	turnOn(TRK1)
	turnOn(TRK2)

def elevate():
	print "elevating"
	turnOn(RGT_TRK1)
	turnOn(LFT_TRK1)
	turnOff(RGT_TRK2)
	turnOff(LFT_TRK2)

def descend():
	print "descending"
	turnOn(RGT_TRK2)
	turnOn(LFT_TRK2)
	turnOff(RGT_TRK1)
	turnOff(LFT_TRK1)

def stop_vertical():
	print "stopping vertical"
	turnOn(RGT_TRK1)
	turnOn(LFT_TRK1)
	turnOn(RGT_TRK2)
	turnOn(LFT_TRK2)

#***************************************************************
#***************************************************************
#***************************************************************


#returns 0 if in tolerance
#returns -1 if less than
#returns 1 if greater than
def is_in_tolerance(val, goal, tol):
	if(abs(val - goal) <= tol):
		return 0
	elif (val < goal):
		return -1
	else:
		return 1

def set_lin_actuator(distance):
	extending = False
	retracting = False
	tolerance = 10
	result = is_in_tolerance(get_lin_feedback(), distance, tolerance)
	while (result != 0):
		if(result == -1 and (extending == False)):
			extend_lin_actuator()
			extending = True
			retracting = False
		elif(result == 1 and (retracting == False)):
			retract_lin_actuator()
			retracting = True
			extending = False

		result = is_in_tolerance(get_lin_feedback(), distance, tolerance)
	stop_lin_actuator()
		

def set_track_actuator(distance):
	extending = False
	retracting = False
	tolerance = 10
	result = is_in_tolerance(get_track_feedback(), distance, tolerance)
	while (result != 0):
		if(result == -1 and (extending == False)):
			extend_track_actuator()
			extending = True
			retracting = False
		elif(result == 1 and (retracting == False)):
			retract_track_actuator()
			retracting = True
			extending = False

		result = is_in_tolerance(get_track_feedback(), distance, tolerance)
	stop_track_actuator()

#using string potentiometer
def set_vertical(distance):
	extending = False
	retracting = False
	tolerance = 10
	result = is_in_tolerance(get_vertical_feedback(), distance, tolerance)
	while (result != 0):
		if(result == -1 and (extending == False)):
			elevate()
			extending = True
			retracting = False
		elif(result == 1 and (retracting == False)):
			descend()
			retracting = True
			extending = False

		result = is_in_tolerance(get_vertical_feedback(), distance, tolerance)
	stop_vertical()

def set_vertical2(level):
	pin = LEVELS[level]

	if (level == CURRENT_LEVEL):
		return
	elif(level < CURRENT_LEVEL):
		elevate()
	else:
		descend()

	while(not(GPIO.input(pin))):
		pass
	stop_vertical()


def pull_to_zero_lin():
	print "pulling to zero lin"
	set_lin_actuator(MIN_DISTANCE_LIN)

def pull_to_zero_track():
	print "pulling to zero track"
	set_track_actuator(MIN_DISTANCE_TRACK)

def pull_to_zero():
	pull_to_zero_lin()
	pull_to_zero_track()


def calibrate():
	print "calibrating"

	extend_lin_actuator()
	wait(0.5)
	#while (not(GPIO.input(C_BUTTON))):
		#pass
	while (get_current_feedback() < 80):
		pass

	stop_lin_actuator()
	MAX_DISTANCE = get_lin_feedback() - 5
	print MAX_DISTANCE
	pull_to_zero_lin()


def pull_wait_push(xDis1, xDis2, seconds):
	set_track_actuator(xDis1)
	wait(1)
	set_lin_actuator(MAX_DISTANCE_LIN)
	wait(1)
	set_track_actuator(xDis2)
	wait(1)
	set_track_actuator(MAX_DISTANCE_LIN - PULL_OUT)
	wait(seconds)
	set_track_actuator(MAX_DISTANCE_LIN)
	wait(1)
	set_track_actuator(xDis1)
	wait(1)
	set_track_actuator(MIN_DISTANCE_LIN)
	wait(1)


def push_psu(xDis):
	set_track_actuator(xDis)
	wait(1)
	set_lin_actuator()
