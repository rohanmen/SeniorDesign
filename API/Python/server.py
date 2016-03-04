import json
import time
import urllib2
#import commands
import subprocess

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


while True:

	try:
		data = json.load(urllib2.urlopen(URL))
		print data

		if(data['type'] == 'pull_psu'):
			print 'pull_psu', data['psu_id']
			index = int(data['psu_id'])
			pull_psu(coordinates[index]['x'])

		elif(data['type'] == 'push_psu'):
			print 'push_psu', data['psu_id']
		elif(data['type'] == 'wait'):
			print 'waiting', data['id'], 'seconds'
	except:
		print 'no connection'


	time.sleep(5)
