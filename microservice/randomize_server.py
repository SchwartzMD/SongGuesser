# -------------------------------------------------------------------
#
# Title: randomize_server
# Author: Harry Hadland
# Description: Creates a TCP server socket for randomize microservice
#
# -------------------------------------------------------------------

# import socket, json, and random libraries
from socket import *
import json
import random

# create server port number - will run on localhost
serverPort = 10001

# create TCP socket via SOCK_STREAM parameter and bind it to the designated server port
server_socket = socket(AF_INET,SOCK_STREAM)
server_socket.bind(("",serverPort))

# have server listen in 1 second intervals
server_socket.listen(1)
print("The server is on and ready to receive.")

# keeps server running
while True:

    # receive data sent from client
    connection_socket, addr = server_socket.accept()
    client_data = connection_socket.recv(10500)

    # load into a json dictionary and transfer array into obj_array
    client_data = json.loads(client_data.decode())
    obj_array = client_data.get("client")


    obj_array_length = len(obj_array)
    pointer = random.randint(0, obj_array_length-1)
    random_obj = []
    random_obj.append(obj_array[pointer])


    # send it back to the client
    server_data = json.dumps({"server":random_obj})
    connection_socket.send(server_data.encode())

    # close out connection
    connection_socket.close()

