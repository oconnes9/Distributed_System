import sys
import socket
import select
import re
import threading

HOST = 'localhost'
SOCKET_LIST = []
RECV_BUFFER = 2048
PORT = 1234
server1Files = []
server2Files = []
found1 = False
found2 = False
serverHost = 'localhost'

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
    def run(self):
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            message = self.csocket.recv(RECV_BUFFER)
            print(message)
            message2 = message.split()
            if message2[0] == 'FindFile:':
                fileName = message2[1]
                for i in server1Files:
                    if fileName == i.name:
                        if i.primary == server1Files:
                            print('found')
                            serverPort = '1111'
                            print('File found.')
                            locationMessage = 'HOST: ', serverHost, ' PORT: ', serverPort, '\n'
                            locationMessage2 = ''.join(locationMessage)
                            self.csocket.send(locationMessage2)
                            break
            
                                    
                for j in server2Files:
                    if fileName == j.name:
                        if j.primary == server2Files:
                            print('found')
                            serverPort = '2222'
                            print('File found.')
                            locationMessage = 'HOST: ', serverHost, ' PORT: ', serverPort, '\n\n'
                            locationMessage2 = ''.join(locationMessage)
                            self.csocket.send(locationMessage2)
                            #else:
                            break

                            
                            # break
        
                locationMessage2 = 'File not found.'
                    #self.csocket.send(locationMessage2)
            elif message2[0] == 'UNLOCK:':
                fileName = message2[1]
                for i in server1Files:
                    if fileName == i.name:
                        if i.lock == 1:
                            i.lock = 0
                            print('released')
                            break
                for j in server2Files:
                    if fileName == j.name:
                        if j.lock == 1:
                            j.lock = 0
                            print('released')
                            break
                break

            elif message2[0] == 'LOCK:':
                fileName = message2[1]
                for i in server1Files:
                    if fileName == i.name:
                        if i.primary == server1Files:
                            foundPrimary = True
                            currPrimary = server1Files
                            index = server1Files.index(i)
                            print ('1')

                for j in server2Files:
                    if fileName == j.name:
                        if j.primary == server2Files:
                            foundPrimary = True
                            currPrimary = server2Files
                            index = server2Files.index(j)
                            print ('2')
                            
                if (foundPrimary):
                    if currPrimary[index].lock == 0:
                        print ('3')
                        currPrimary[index].lock = 1
                        print('locked')
                        self.csocket.send('LOCKED\n')
                        foundPrimary = False;
                        break
                    else:
                        print ('4')
                        print('busy')
                        self.csocket.send('BUSY\n')
                        foundPrimary = False
                        break


                #ocationMessage2 = 'File does not exist'
                #self.csocket.send(locationMessage2)
# break
#else:


class file(object):
    def __init__(self, name=None, lock=None, primary=None):
        self.name = name
        self.lock = lock
        self.primary = primary

def ProxyServ():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind((HOST, PORT))
    file1 = file('ascii.txt', 0, server1Files)
    file2 = file('ascii2.txt', 0, server1Files)
    file3 = file('outputFile.txt', 0, server1Files)
    server1Files.append(file1)
    server1Files.append(file2)
    server1Files.append(file3)
    server2Files.append(file3)
    print("Directory started")
    print("Waiting for client request..")
    while True:
        proxy.listen(1)
        clientsock, clientAddress = proxy.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()

if __name__ == "__main__":
    
    sys.exit(ProxyServ())