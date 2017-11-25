
import sys
import socket
import select
import os

def client():
    directoryHost = 'localhost'
    directoryPort = 1111
    serverPort = 0
    serverHost = ''
    fileName = raw_input("Enter the name of the file you want access to: ")
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.settimeout(20)
    message = 'FindFile: ', fileName
    message2 = ''.join(message)
    try :
        p.connect((directoryHost, directoryPort))
    except :
        print 'Unable to connect to directory.'
        sys.exit()
    
    print 'Connected to directory.'
    p.send(message2)
    #f = open("received", 'wb')

    while 1:
        socket_list = [sys.stdin, p]
            
            # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        
        for sock in ready_to_read:
            if sock == p:
                # incoming message from remote server, s
                location = sock.recv(2048)
                if not location :
                    print '\nDisconnected from proxy'
                    sys.exit()
                else :
                    location2 = location.split()
                    if location2[0] == "HOST:":
                        serverHost = location2[1]
                        serverPort = int(location2[3])
                        print "Found Location: "
                        print(serverHost, serverPort)
                        message = 'Request: ', fileName
                        message2 = ''.join(message)
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        #self.s.settimeout(20)
                        try :
                            s.connect((serverHost, serverPort))
                        except :
                            print 'Unable to connect'
                            sys.exit()
        
                        print 'Connected to server.'
                        s.send(message2)
                        socket_list = [sys.stdin, s]
        
                        # Get the list sockets which are readable
                        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        
                        for sock in ready_to_read:
                            if sock == s:
                                # incoming message from remote server, s
                                filepath = os.path.join('/Users/Sean/Documents/ClientStorage/', fileName)
                                f = open(fileName, 'w')
                                l = sock.recv(2048)
                                while(l):
                                    print('receiving..')
                                    print l
                                    f.write(l)
                                    l = sock.recv(2048)
                                f.close()
                                print "Done receiving and sending"
                                sock.close

                    else:
                        print("File not in directory.")
                        sock.close

                        
                    
        
            else :
                # user entered a message
                fileName = sys.stdin.readline()
                message = 'FindFile: ', fileName
                message2 = ''.join(message)
                p.send(message2)
                sys.stdout.flush()

if __name__ == "__main__":
    
    sys.exit(client())