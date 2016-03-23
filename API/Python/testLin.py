import commands

LIN1 = 35
LIN1 = 37
DELAY = 0.25

commands.setup()


print commands.get_lin_feedback()

while True:

	time = 0;
	commands.extend_lin_actuator()
	while time < 5:
		print commands.get_lin_feedback()
		commands.wait(DELAY)
		time = time + DELAY

	commands.wait(1)

	time = 0;
	commands.retract_lin_actuator()
	while time < 5:
		print commands.get_lin_feedback()
		commands.wait(DELAY)
		time = time + DELAY

