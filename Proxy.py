import sys
import socket
import select
import re
import threading

HOST = 'localhost'
SOCKET_LIST = []
RECV_BUFFER = 2048
ClientPORT = 8008
ServerPORT = 7007

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
    def run(self):
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        while True:
            message = self.csocket.recv(RECV_BUFFER)
            message2 = message.split()
            if message2[0] == 'ClientRequest:':
                fileDirectory = message2[1]
                message3 = 'ProxyRequest: ', fileDirectory
                message4 = ''.join(message3)
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.settimeout(2)
                try :
                    self.s.connect((HOST, ServerPORT))
                except :
                    print 'Unable to connect'
                    sys.exit()
    
                print 'Connected to server.'
                self.s.send(message4)
                while 1:
                    socket_list = [sys.stdin, s]
        
                    # Get the list sockets which are readable
                    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        
                    for sock in ready_to_read:
                        if sock == s:
                                # incoming message from remote server, s
                            file = self.s.recv(2048)
                            if not file :
                                print '\nDisconnected from Server'
                                sys.exit()
                            else :
                                while(file):
                                    file = file + self.s.recv(2048)
                                    print "Done receiving"
                                self.s.close
                                self.csocket.send(file)
        
        
            else:
                break
        
        print ("Client at ", clientAddress , " disconnected...")


def ProxyServ():
    print('hi')
    proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy.bind((HOST, ClientPORT))
    print("Proxy started")
    print("Waiting for client request..")
    while True:
        proxy.listen(1)
        clientsock, clientAddress = proxy.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()

if __name__ == "__main__":
    
    sys.exit(ProxyServ())