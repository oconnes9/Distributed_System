
import sys
import socket
import select
import os.path

directoryHost = 'localhost'
directoryPort = 1234
serverPort = 0
serverHost = ''
cd = ''
clientDirectoryString = '/Users/Sean/Documents/ClientStorage/'
clientDirectory = os.listdir(clientDirectoryString)

def Proxy(fileName1):
    #fileName1 = raw_input("Enter the name of the file you want access to: ")
    fileName2 = [fileName1, '.txt']
    fileName = ''.join(fileName2)
    if fileName not in clientDirectory:
        directoryConnect(fileName)
    else:
        onClient(fileName)

def onClient(fileName):
    fileDirectory = [clientDirectoryString, fileName]
    fileDirectory2 = ''.join(fileDirectory)
    f = open(fileDirectory2, "r")
    print f
    edit = raw_input("Do you want to edit? yes or no")
    if edit == 'yes':
        f = open(fileDirectory2, "w")
        updated = raw_input("Write out new file here.")
        f.write(updated)
        
    elif edit == 'no':
        print("Not updated")
    f.close()

def directoryConnect(fileName):
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
        
        #while 1:
    socket_list = [sys.stdin, p]
        
        # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        
    for sock in ready_to_read:
        print('helllllo')
        if sock == p:
            # incoming message from remote server, s
            location = sock.recv(2048)
            if not location :
                p.disconnect
                print '\nDisconnected from directory.'
                sys.exit()
            else :
                location2 = location.split()
                if location2[0] == "HOST:":
                    serverHost = location2[1]
                    serverPort = int(location2[3])
                    print "Found Location: "
                    print(serverHost, serverPort)
                    serverConnect(serverHost, serverPort, fileName)
                else:
                    print("File not in directory.")
                    sock.close()




        else :
            # user entered a message
            print("Enter a filename.")
            fileName = sys.stdin.readline()
            message = 'FindFile: ', fileName
            message2 = ''.join(message)
            p.send(message2)
            sys.stdout.flush()
    return;
#print('waiting..')
#sock.close()

#cD = [clientDirectoryString, fileName]
# currentDirectory = ''.join(cD)

def serverConnect(serverHost, serverPort, fileName):
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
        #while 1:
    s.send(message2)
    socket_list = [sys.stdin, s]
    
    # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    
    for sock in ready_to_read:
        if sock == s:
            # incoming message from remote server, s
            #filepath = os.path.join('/Users/Sean/Documents/ClientStorage/', fileName)
            #f = open(filepath, 'w')
            l = sock.recv(2048)
            #while(l):
            print l
            #l = sock.recv(2048)
            print 'hi'
            
            #f.close()
            edit = raw_input("Done receiving. Do you want to edit? yes or no\n")
            if edit == 'yes':
                updated = raw_input("Write out new file here.")
                updateMessage = ["FILE_UPDATE: ", fileName, " NEW_DATA: ", updated, "\n"]
                updatedMessage2 = ''.join(updateMessage)
                sock.send(updatedMessage2)
            elif edit == 'no':
                notUpdated = "NO_UPDATE"
                sock.send(notUpdated)
            sock.close()
    #s.close()
    return;


#if __name__ == "__main__":
    
#  sys.exit(Proxy())