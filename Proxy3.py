
import sys
import socket
import select
import os.path
import datetime
import random

directoryHost = 'localhost'
directoryPort = 1234
serverPort = 0
serverHost = ''
cd = ''
clientDirectoryString = '/Users/Sean/Documents/ClientStorage3/'
clientDirectory = os.listdir(clientDirectoryString)
cacheDirectoryString = '/Users/Sean/Documents/ClientStorage3/Cache/'
cacheDirectory = os.listdir(clientDirectoryString)
cache = []
version = []
serverHost1 = ''
serverPort1 = 0

def Proxy(fileName1):
    
    #fileName1 = raw_input("Enter the name of the file you want access to: ")
    fileName2 = [fileName1, '.txt']
    fileName = ''.join(fileName2)
    if fileName in clientDirectory:
        onClient(fileName)
    
    elif fileName in cache:
        directoryConnect2(fileName)
    
    else:
        directoryConnect(fileName)

#cache.update(, fileName)
def updateCacheVersion(fileName, l, s, shost1, sport1):
    message = 'Request: ', fileName
    message2 = ''.join(message)
    s.send(message2)
    socket_list = [sys.stdin, s]
    
    # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    fileDirectory = [cacheDirectoryString, fileName]
    fileDirectory2 = ''.join(fileDirectory)
    file = open(fileDirectory2, 'w')
    for sock in ready_to_read:
        if sock == s:
            # incoming message from remote server, s
            #filepath = os.path.join('/Users/Sean/Documents/ClientStorage/', fileName)
            #f = open(filepath, 'w')
            l = sock.recv(2048)
            l2 = l.split()
            length = len(l2)
            version1 = int(l2[1])
            newData = l2[2]
            x = 3
            while (x!=length):
                newData = newData + ' ' + l2[x]
                x = x + 1
            file.write(newData)
            #while(l):
            version[cache.index(fileName)] = version1
            onCache(fileName, shost1, sport1)
    s.close()

def addToCache(fileName, version1):
    if len(cache) == 2:
        newName = cache[1]
        fileDirectory = [cacheDirectoryString, newName]
        fileDirectory2 = ''.join(fileDirectory)
        os.remove(fileDirectory2)
        #fileDirectory3 = os.listdir(fileDirectory2)
        cache.insert(0, fileName)
        version.insert(0, version1)
        cache.pop()
        version.pop()
    
    elif len(cache) < 2:
        cache.insert(0, fileName)
        version.insert(0, version1)

def onCache(fileName, shost1, sport1):
    unlock(fileName)
    fileDirectory = [cacheDirectoryString, fileName]
    fileDirectory2 = ''.join(fileDirectory)
    f = open(fileDirectory2, "r")
    contents = f.read()
    print (contents)
    locking = 0
    edit = raw_input("Do you want to edit? yes or no")
    if edit == 'yes':
        while locking == 0:
            locking = lock(fileName)
        f = open(fileDirectory2, "w")
        updated = raw_input("Write out new file here.")
        f.write(updated)
        version[cache.index(fileName)] = version[cache.index(fileName)] + 1
        updateVersion(fileName, updated, shost1, sport1)
        locking = 0
    
    elif edit == 'no':
        print("Not updated")
    f.close()

    version1 = version[cache.index(fileName)]
    del version[cache.index(fileName)]
    cache.remove(fileName)
    cache.insert(0, fileName)
    version.insert(0, version1)

def onClient(fileName):
    fileDirectory = [clientDirectoryString, fileName]
    fileDirectory2 = ''.join(fileDirectory)
    f = open(fileDirectory2, "r")
    contents = f.read()
    print (contents)
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
        print ('Unable to connect to directory.')
        sys.exit()
    
    print ('Connected to directory.')

    p.send(message2)
    #while 1:
    socket_list = [sys.stdin, p]
    
    # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    
    for sock in ready_to_read:
        if sock == p:
            # incoming message from remote server, s
            mess = sock.recv(2048)
            print(mess)
            if not mess :
                sock.close()
                print ('\nDisconnected from directory.')
                sys.exit()
            else :
                mess2 = mess.split()
                if mess2[0] == "HOST:":
                    serverHost = mess2[1]
                    serverPort = int(mess2[3])
                    print ("Found Location: ")
                    print(serverHost, serverPort)
                    serverConnect(serverHost, serverPort, fileName)
                
                else:
                    print("File not in directory.")
                    sock.close()

    p.close()
    
    return;

def directoryConnect2(fileName):
    print('directoryConnect')
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.settimeout(20)
    message = 'FindFile: ', fileName
    message2 = ''.join(message)
    try :
        p.connect((directoryHost, directoryPort))
    except :
        print ('Unable to connect to directory.')
        sys.exit()
    
    print ('Connected to directory.')
    p.send(message2)
    #while 1:
    socket_list = [sys.stdin, p]
    
    # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    
    for sock in ready_to_read:
        if sock == p:
            # incoming message from remote server, s
            mess = sock.recv(2048)
            print(mess)
            if not mess :
                sock.disconnect
                print ('\nDisconnected from directory.')
                sys.exit()
            else :
                mess2 = mess.split()
                if mess2[0] == "HOST:":
                    serverHost1 = mess2[1]
                    serverPort1 = int(mess2[3])
                    print ("Found Location: ")
                    print(serverHost1, serverPort1)
                
                else:
                    print("File not in directory.")
                    sock.close()

    p.close()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self.s.settimeout(20)
    try :
        s.connect((serverHost1, serverPort1))
    except :
        print ('Unable to connect to server1')
        sys.exit()
    
    print ('Connected to server.')
    #while 1:
    message = 'VersionCheck: ', fileName
    message2 = ''.join(message)
    s.send(message2)
    socket_list = [sys.stdin, s]
    
    # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    fileDirectory = [cacheDirectoryString, fileName]
    fileDirectory2 = ''.join(fileDirectory)
    file = open(fileDirectory2, 'w')
    for sock in ready_to_read:
        if sock == s:
            # incoming message from remote server, s
            #filepath = os.path.join('/Users/Sean/Documents/ClientStorage/', fileName)
            #f = open(filepath, 'w')
            l = sock.recv(2048)
            if l == str(version[cache.index(fileName)]):
                onCache(fileName, serverHost1, serverPort1)
                break
            else:
                updateCacheVersion(fileName, l, s, serverHost1, serverPort1) #DOOOOOOOOOOOOOOOOOOOOOO THISSSSSSSSSSSSSS
                break

    serverHost1 = ''
    serverPort1 = 0
    
    return;
#print('waiting..')
#sock.close()

#cD = [clientDirectoryString, fileName]
# currentDirectory = ''.join(cD)
def updateVersion(fileName, updated, shost1, sport1):
    print(shost1)
    message = 'VERSION_UPDATE: ', fileName, ' DATA: ', updated, '\n'
    message2 = ''.join(message)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self.s.settimeout(20)
    try :
        s.connect((shost1, sport1))
    except :
        print ('Unable to connect')
        sys.exit()
    print('updating')
    s.send(message2)
    s.close()
    unlock(fileName)



def unlock(fileName):
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #p.settimeout(20)
    print("unlocking")
    message = 'UNLOCK: ', fileName
    message2 = ''.join(message)
    try :
        p.connect((directoryHost, directoryPort))
    except :
        print ('Unable to connect to directory.')
        sys.exit()
    
    p.send(message2)
    p.close()

def lock(fileName):
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #p.settimeout(20)
    message = 'LOCK: ', fileName
    message2 = ''.join(message)
    try :
        p.connect((directoryHost, directoryPort))
    except :
        print ('Unable to connect to directory.')
        sys.exit()
    waiting = 1
    while waiting == 1:
        print('loop')
        p.send(message2)
        #while 1:
        socket_list = [sys.stdin, p]
        
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        
        for sock in ready_to_read:
            if sock == p:
                # incoming message from remote server, s
                mess = sock.recv(2048)
                print(mess)
                if not mess :
                    sock.disconnect
                    print ('\nDisconnected from directory.')
                    sys.exit()
                else :
                    mess2 = mess.split()
                    if mess2[0] == "LOCKED":
                        p.close()
                        return 1;
                    elif mess2[0] == "BUSY":
                        return 0;

    p.close()


def getOtherServers(fileName):
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.settimeout(20)
    message = 'GetAllServers: ', fileName
    message2 = ''.join(message)
    try :
        p.connect((directoryHost, directoryPort))
    except :
        print ('Unable to connect to directory.')
        sys.exit()
    
    print ('Connected to directory.')

    p.send(message2)
    #while 1:
    socket_list = [sys.stdin, p]
    
    # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    
    for sock in ready_to_read:
        if sock == p:
            # incoming message from remote server, s
            mess = sock.recv(2048)
            print(mess)
            if not mess :
                sock.close()
                print ('\nDisconnected from directory.')
                sys.exit()
            else :
                serverList = mess
                sock.close()
                return serverList



def serverConnect(serverHost, serverPort, fileName):
    message = 'Request: ', fileName
    message2 = ''.join(message)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #self.s.settimeout(20)
    try :
        s.connect((serverHost, serverPort))
    except :
        print ('Unable to connect')
        sys.exit()
    
    print ('Connected to server.')
    #while 1:
    s.send(message2)
    socket_list = [sys.stdin, s]
    
    # Get the list sockets which are readable
    ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
    fileDirectory = [cacheDirectoryString, fileName]
    fileDirectory2 = ''.join(fileDirectory)
    file = open(fileDirectory2, 'w')
    for sock in ready_to_read:
        if sock == s:
            # incoming message from remote server, s
            #filepath = os.path.join('/Users/Sean/Documents/ClientStorage/', fileName)
            #f = open(filepath, 'w')
            l = sock.recv(2048)
            l2 = l.split()
            length = len(l2)
            print(l2[1])
            version1 = int(l2[1])
            newData = l2[2]
            x = 3
            while (x!=length):
                newData = newData + ' ' + l2[x]
                x = x + 1
            file.write(newData)
            file.close()
            #while(l):
            print(newData)
            #l = sock.recv(2048)
            locking = 0
            #f.close()
            edit = raw_input("Done receiving. Do you want to edit? yes or no\n")
            if edit == 'yes':
                while locking == 0:
                    locking = lock(fileName)
                file = open(fileDirectory2, 'w')
                updated = raw_input("Write out new file here.")
                servers = getOtherServers(fileName)
                print(servers)
                servers2 = servers.split()
                i = 0
                while i < len(servers2):
                    serverPort = int(servers2[i])
                    #print(serverPort)
                    updateVersion(fileName, updated, serverHost, serverPort)
                    i = i+1
                #updateVersion(fileName, updated, serverHost, serverPort)
                version1 = version1 + 1
                file.write(updated)
                #updateVersion(fileName, updated)
                #updateMessage = ["FILE_UPDATE: ", fileName, " NEW_DATA: ", updated, "\n"]
                #updatedMessage2 = ''.join(updateMessage)
                file.close()
                locking = 0
            
            elif edit == 'no':
                notUpdated = "NO_UPDATE"
                sock.send(notUpdated)
            
            sock.close()



    addToCache(fileName, version1)
    #s.close()
    return;
#if __name__ == "__main__":

#  sys.exit(Proxy())