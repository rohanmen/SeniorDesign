import commands

DELAY = 2
commands.setup()

while True:
	print commands.get_track_feedback()
	commands.wait(DELAY)