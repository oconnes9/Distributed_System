import sys
import socket
import select
import re
import threading

HOST = 'localhost'
SOCKET_LIST = []
RECV_BUFFER = 2048
PORT = 1234
server1Files = ['ascii.txt', 'ascii2.txt']
server2Files = ['outputFile.txt']

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
    def run(self):
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            message = self.csocket.recv(RECV_BUFFER)
            message2 = message.split()
            if message2[0] == 'FindFile:':
                fileName = message2[1]
                if fileName in server1Files:
                    serverHost = 'localhost'
                    serverPort = '1111'
                    print('File found.')
                    locationMessage = 'HOST: ', serverHost, ' PORT: ', serverPort, '\n'
                    locationMessage2 = ''.join(locationMessage)
                elif fileName in server2Files:
                    serverHost = 'localhost'
                    serverPort = '2222'
                    print('File found.')
                    locationMessage = 'HOST: ', serverHost, ' PORT: ', serverPort, '\n\n'
                    locationMessage2 = ''.join(locationMessage)
                else:
                    locationMessage2 = 'File not found.'
            
                self.csocket.send(locationMessage2)
            break


def ProxyServ():
    print('hi')
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind((HOST, PORT))
    print("Directory started")
    print("Waiting for client request..")
    while True:
        proxy.listen(1)
        clientsock, clientAddress = proxy.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()

if __name__ == "__main__":
    
    sys.exit(ProxyServ())