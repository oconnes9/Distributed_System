import sys
import socket
import select
import re
import threading
import os

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 2048
PORT = 2222
directory = '/Users/Sean/Documents/Server2/'

class ProxyThread(threading.Thread):
    def __init__(self,proxyAddress,proxysocket):
        threading.Thread.__init__(self)
        self.psocket = proxysocket
    def run(self):
        newData = ''
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            message = self.psocket.recv(RECV_BUFFER)
            print message
            message2 = message.split()
            if message2[0] == 'Request:':
                fileName = message2[1]
                fileDirectory = directory, fileName
                fileDirectory2 = ''.join(fileDirectory)
                f = open(fileDirectory2, "r")
                l = f.read(2048)
                while (l):
                    print('sending..')
                    self.psocket.send(l)
                    l = f.read(2048)
                f.close()
            elif message2[0] == "FILE_UPDATE:":
                fileName = message2[1]
                fileDirectory = directory, fileName
                fileDirectory2 = ''.join(fileDirectory)
                length = len(message2)
                x = 3
                while (x!=length):
                    newData = newData + ' ' + message2[x]
                    x = x + 1
                f = open(fileDirectory2, "w")
                f.write(newData)
                newData = ''
                f.close()
            
            elif message2[0] == "NO_UPDATE:":
                print('Unmodified')
            
            else:
                break

        print ("Client has disconnected...")
        print ("waiting..")



def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    print("Server started")
    print("Waiting for proxy request..")
    while True:
        server.listen(1)
        proxysock, proxyAddress = server.accept()
        newthread = ProxyThread(proxyAddress, proxysock)
        newthread.start()

if __name__ == "__main__":
    
    sys.exit(Server())