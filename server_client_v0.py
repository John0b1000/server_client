# file: server_client_v0.py
#

# version: 0
# establishing multiple threads so that a single node can act as both a client
# and a server
#

# sources:
#
# https://www.geeksforgeeks.org/multithreading-python-set-1/
#
# https://stackoverflow.com/questions/43419566/creating-threads-within-a-thread-in-python
#
# https://www.geeksforgeeks.org/python-communicating-between-threads-set-1/#:~:text=Perhaps%20the%20safest%20way%20to,in%20the%20code%20given%20below.
#

import sys
import socket
import threading
import pickle
import time

def server_init(port, server):
    
    # define variables
    #
    PORT = port
    SERVER = server
    ADDR = (SERVER, PORT)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(ADDR)
    serverSocket.listen()
    print("\nInitializing server ...")
    print(f"Server is listening on {SERVER}")

    while True:
        connection, addr = serverSocket.accept()
        thread = threading.Thread(target=handleClient, args=(connection, addr))
        thread.start()

def handleClient(connection, addr):

    LENGTH = 2048
    
    div = "-"
    print('\n')
    print(div.ljust(80,"-"))
    print()
    print(f"New connection - {addr}")
    connected = True
    while connected:
        msg_in = pickle.loads(connection.recv(LENGTH))
        print("\nMessage received!\n")
        print("Message contents: {0}".format(msg_in))
        print()
        connected = False
    connection.close()
    print(f"Connection closed - {addr}")
    print()
    print(div.ljust(80,"-"))
    print()

def client_init():

    # ask user for destination port and ip
    #
    time.sleep(1)
    print()
    PORT = int(input("Enter port: "))
    SERVER = input("Enter ip: ")
    ADDR = (SERVER, PORT)

    # enter a message to send
    #
    while True:
        msg = input("Enter a message to send: ")
        if (msg != "quit"):
            picklemsg = pickle.dumps(msg)
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect(ADDR)
            clientSocket.send(picklemsg)
        else:
            print("Client closed.")
            break

# program: main
#
def main(argv):

    # start the server first
    #
    ts = threading.Thread(target=server_init, args=(int(argv[1]), argv[2]))
    tc = threading.Thread(target=client_init)

    ts.start()
    tc.start()

# begin gracefully
#
if __name__ == "__main__":
    main(sys.argv)

#
# end of file
