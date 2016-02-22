from commands import *

setup()

while True:
	move_servo(0,180)
	wait(2)
	move_servo(180,0)
	wait(2)