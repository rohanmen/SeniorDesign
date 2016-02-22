from commands import *


while True:
	distance = get_ir_distance(channel)
	print distance, "cm"
	wait(1)