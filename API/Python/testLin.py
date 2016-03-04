import commands

LIN1 = 35
LIN1 = 37

commands.setup()

while True:
	commands.extend_lin_actuator()
	wait(5)
	commands.retract_lin_actuator()
	wait(5)

