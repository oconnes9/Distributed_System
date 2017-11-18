import sys
import socket
import select
import re
import threading
import os

HOST = 'localhost'
SOCKET_LIST = []
RECV_BUFFER = 2048
PORT = 7007

class ProxyThread(threading.Thread):
    def __init__(self,proxyAddress,proxysocket):
        threading.Thread.__init__(self)
        self.psocket = proxysocket
    def run(self):
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            message = self.psocket.recv(RECV_BUFFER)
            message2 = message.split()
            if message2[0] == 'ProxyRequest:':
                fileDirectory = message2[1]
                file = open(direct+fileDirectory, "r")
                self.psocket.send(file)

            else:
                break

        print ("Client at ", clientAddress , " disconnected...")




def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    print("Server started")
    print("Waiting for proxy request..")
    while True:
        server.listen(1)
        proxysock, proxysock = server.accept()
        newthread = ProxyThread(proxyAddress, proxysock)
        newthread.start()

if __name__ == "__main__":
    
    sys.exit(Server())