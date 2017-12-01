import Proxy2
import sys
import select

def Client2():
    
    while 1:
        fileName = raw_input("Enter the name of the file you want access to: ")
        Proxy2.Proxy(fileName)
#Proxy.GetLocation(fileName)

#fileName = raw_input("Enter the name of the file you want access to: ")
#Proxy.Proxy(fileName)






if __name__ == "__main__":
    
    sys.exit(Client2())