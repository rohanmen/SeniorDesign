import os
import json
import socket


def sendMessage(ip, port, message):
	request_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	request_sender.connect((ip, port))
	request_sender.sendall(message)
	request_sender.close()

with open("config.json") as json_file:
	server_data = json.load(json_file)

ip = server_data["ip"]
port = server_data["port"]

print ip, port

#request_sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#request_sender.connect((ip, port))
#request_sender.sendall("hi this is a test")

while True:
	text = raw_input()

	if(text == 'exit'):
		break
	sendMessage(ip, port, text)



