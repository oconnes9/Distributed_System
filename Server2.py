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
server2Files = []

class ProxyThread(threading.Thread):
    def __init__(self,proxyAddress,proxysocket):
        threading.Thread.__init__(self)
        self.psocket = proxysocket
    def run(self):
        newData = ''
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            message = self.psocket.recv(RECV_BUFFER)
            print (message)
            message2 = message.split()
            
            if message2[0] == 'Request:':
                fileName = message2[1]
                for j in server2Files:
                    if fileName == j.name:
                        version = j.version
                fileDirectory = directory, fileName
                fileDirectory2 = ''.join(fileDirectory)
                f = open(fileDirectory2, "r")
                l = f.read(2048)
                message = ["Version: ", str(version), ' ', l]
                message2 = ''.join(message)
                print('sending..')
                self.psocket.send(message2)
                f.close()
                break
            elif message2[0] == "FILE_UPDATE:":
                fileName = message2[1]
                fileDirectory = directory, fileName
                fileDirectory2 = ''.join(fileDirectory)
                length = len(message2)
                newData = message2[3]
                x = 4
                while (x!=length):
                    newData = newData + ' ' + message2[x]
                    x = x + 1
                f = open(fileDirectory2, "w")
                f.write(newData)
                
                newData = ''
                f.close()
                break
                    
            elif message2[0] == 'VERSION_UPDATE:':
                fileName = message2[1]
                for j in server2Files:
                    if fileName == j.name:
                        j.version = j.version + 1
                        print('updated')
                        fileDirectory = directory, fileName
                        fileDirectory2 = ''.join(fileDirectory)
                        length = len(message2)
                        newData = message2[3]
                        x = 4
                        while (x!=length):
                            newData = newData + ' ' + message2[x]
                            x = x + 1
                        f = open(fileDirectory2, "w")
                        f.write(newData)
                        newData = ''
                        f.close()
                        break
                
            elif message2[0] == 'VersionCheck:':
                fileName = message2[1]
                for i in server2Files:
                    if fileName == i.name:
                        version = i.version
                        self.psocket.send(str(version))
                    
            elif message2[0] == "NO_UPDATE:":
                print('Unmodified')
                break
            
            else:
                break

        print ("Client has disconnected...")

class file(object):
    def __init__(self, name=None, version=None):
        self.name = name
        self.version = version

def Server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    direct = os.listdir(directory)
    for item in direct:
        file1 = file(item, 0)
        server2Files.append(file1)
    print("Server started")
    print("Waiting for proxy request..")
    while True:
        server.listen(1)
        proxysock, proxyAddress = server.accept()
        newthread = ProxyThread(proxyAddress, proxysock)
        newthread.start()

if __name__ == "__main__":
    
    sys.exit(Server())