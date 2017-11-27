import Proxy
import sys
import select

def Client():
    
    while 1:
        fileName = raw_input("Enter the name of the file you want access to: ")
        Proxy.Proxy(fileName)

#fileName = raw_input("Enter the name of the file you want access to: ")
#Proxy.Proxy(fileName)






if __name__ == "__main__":
    
    sys.exit(Client())