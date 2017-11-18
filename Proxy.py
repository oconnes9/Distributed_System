import sys
import socket
import select
import re
import threading

HOST = ''
SOCKET_LIST = []
RECV_BUFFER = 2048
ClientPORT = 8008
ServerPORT = 7007

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            message = self.csocket.recv(RECV_BUFFER)
            message2 = message.split()
            if message2[0] == 'ClientRequest:':
                fileDirectory = message2[1]
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                try :
                    s.connect((host, ServerPORT))
                except :
                    print 'Unable to connect'
                    sys.exit()
    
    print 'Connected to remote host.'
        
            else:
                break
        
            print ("from client", msg)
            self.csocket.send(bytes(msg,'UTF-8'))
        print ("Client at ", clientAddress , " disconnected...")


def DistributedSystem():
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind((LOCALHOST, ClientPORT))
    print("Proxy started")
    print("Waiting for client request..")
    while True:
        proxy.listen(1)
        clientsock, clientAddress = proxy.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()