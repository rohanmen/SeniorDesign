import json
import time
import urllib2
import commands
import subprocess

commands.setup()

bashCommand = "hostname -I"
process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
IP = process.communicate()[0].split()[0]
#IP =  "172.20.10.3"

PORT = '8080'
URL = 'http://' + IP + ':' + PORT + '/api/command' 
print URL

with open("Python/data.json") as json_file:
    coordinates = json.load(json_file)


def pull_psu(distance):
	print distance


try:
	while True:

		try:
			data = json.load(urllib2.urlopen(URL))
			print data

			if(data['type'] == 'pull_psu'):
				print 'pull_psu', data['psu_id']
				#index = int(data['psu_id'])
				#pull_psu(coordinates[index]['x'])
				commands.pull_psu()

			elif(data['type'] == 'push_psu'):
				print 'push_psu', data['psu_id']
				commands.push_psu()
			elif(data['type'] == 'wait'):
				print 'waiting', data['psu_id'], 'seconds'
				commands.wait(data['psu_id'])
		except:
			print 'no connection'


		time.sleep(5)
finally:
	commands.cleanup()

