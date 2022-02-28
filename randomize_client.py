# -------------------------------------------------------------------
#
# Title: randomize_client
# Author: Harry Hadland
# Description: Creates a client TCP socket connection for microservice
#
# -------------------------------------------------------------------

# import json and socket libraries
import json
from socket import *

# -------------------------------------------------------------------
# Method that generates socket and returns a random object from
# array passed in.
# -------------------------------------------------------------------


def randomObjReturn(client_array):

    # define server name and port
    server_name = "localhost"
    server_port = 10001

    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))

    # encode array in JSON format
    data_sent = json.dumps({"client": client_array})
    client_socket.send(data_sent.encode())

    # capture data sent back from server
    data_received = client_socket.recv(9000)

    # decode into a json dictionary object
    random_object_json = json.loads(data_received.decode())
    random_object = random_object_json.get("server")[0]

    # close socket connection
    client_socket.close()

    return random_object
