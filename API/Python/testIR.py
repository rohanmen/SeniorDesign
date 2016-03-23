import commands

DELAY = 0.25
commands.setup()

while True:
	print commands.get_track_feedback()
	commands.wait(DELAY)