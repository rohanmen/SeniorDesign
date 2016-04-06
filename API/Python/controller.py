import Tkinter as tk
import commands

def onKeyPress(event):
	char = event.char
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
	elif char == 'p':
		print "lin val : " + commands.get_lin_feedback()
		print "track val : " + commands.get_track_feedback()



commands.setup()
root = tk.Tk()
root.geometry('300x200')

root.bind('<KeyPress>', onKeyPress)
#root.bind('<KeyRelease>', onKeyRelease)
root.mainloop()