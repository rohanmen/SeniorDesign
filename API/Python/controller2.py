import Tkinter as tk
import commands

def onKeyPress(char):
	print char

	if char == 'a':
		print "track moving left"
		commands.stop_lin_actuator()
		commands.retract_track_actuator()
	elif char == 'd':
		print "track moving right"
		commands.stop_lin_actuator()
		commands.extend_track_actuator()
	elif char == 'w':
		print "lin extending"
		commands.stop_track_actuator()
		commands.extend_lin_actuator()
	elif char == 's':
		print "lin retracting"
		commands.stop_track_actuator()
		commands.retract_lin_actuator()
	elif char == 'q':
		print "stopping"
		commands.stop_lin_actuator()
		commands.stop_track_actuator()
	elif char == 'i':
		print "going up"
		commands.elevate()
	elif char == 'k':
		print "going donwn"
		commands.descend()
	elif char == 'l':
		print "stopping vertical"
		commands.stop_vertical()
	elif char == 'p':
		print "lin val : " + str(commands.get_lin_feedback())
		print "track val : " + str(commands.get_track_feedback())
		print "vertical val : " + str(commands.get_vertical_feedback())



commands.setup()


while True:
	c = input()
	onKeyPress(c)