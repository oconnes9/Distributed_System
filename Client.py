
import sys
import socket
import select

def client():
    if(len(sys.argv) < 3) :
        print 'Usage : python chat_client.py hostname port'
        sys.exit()
    
    host = sys.argv[1]
    port = int(sys.argv[2])

    fileDirectory = raw_input("Enter the directory of the file you want access to: ")
    p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    p.settimeout(2)
    message = 'ClientRequest: ', fileDirectory
    message2 = ''.join(message)
    try :
        p.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host.'
    p.send(message2)
    f = open(fileDirectory, 'wb')

    while 1:
        socket_list = [sys.stdin, p]
        
        # Get the list sockets which are readable
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])
        
        for sock in ready_to_read:
            if sock == p:
                # incoming message from remote server, s
                file = p.recv(2048)
                if not file :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    while(file):
                        f.write(file)
                        file = p.recv(2048)
                    f.close()
                    print "Done receiving"
                    p.close
        
            else :
                # user entered a message
                fileDirectory = sys.stdin.readline()
                message = 'ClientRequest: ', fileDirectory
                message2 = ''.join(message)
                p.send(message2)
                sys.stdout.flush()

if __name__ == "__main__":
    
    sys.exit(client())