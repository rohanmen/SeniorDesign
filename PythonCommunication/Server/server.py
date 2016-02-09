import os
import json
import socket

with open("config.json") as json_file:
	server_data = json.load(json_file)

ip = server_data["ip"]
port = server_data["port"]

print ip, port

request_handler = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
request_handler.bind(('', port))
request_handler.listen(1)

while True:
	connection, client_address = request_handler.accept()
	data = connection.recv(1024).decode()
	print data
	if(data == 'exit'):
		break
request_handler.close()
