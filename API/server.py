import json
import time
import urllib2

PORT = '8080'
URL = 'http://172.20.10.3:8080/api/command' 
print URL

while True:

	try:
		data = json.load(urllib2.urlopen(URL))
		print data

		if(data['type'] == 'pull_psu'):
			print 'pull_psu', data['psu_id']
		elif(data['type'] == 'push_psu'):
			print 'push_psu', data['psu_id']
	except:
		print 'no connection'


	time.sleep(5)
