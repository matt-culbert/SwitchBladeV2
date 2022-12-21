# Switchblade

# To Use #
There is the C2 and the controller files. The C2 uses Flask to handle beacon requests and then the controller uses gRPC to talk with the Flask server and get updates on command status as well as write new commands

# To Run #

Put the C2 and controller in the same folder. Start the C2 and wait for a beacon to check in. Once a beacon checks in, you can use the controller to send new commands to it as well as get the status on executed commands


# To Generate PB # 

```
python -m grpc_tools.protoc --proto_path=. ./protobuff.proto --python_out=. --grpc_python_out=.
```

# To Generate Certs #

```
openssl genrsa -out ca.key 2048 

openssl req -new -x509 -days 365 -key ca.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=Acme Root CA" -out ca.crt

openssl req -newkey rsa:2048 -nodes -keyout server.key -subj "/C=CN/ST=GD/L=SZ/O=Acme, Inc./CN=_*.example.com" -out server.csr openssl x509 -req -extfile <(printf "subjectAltName=DNS:example.com,DNS:www.example.com") -days 365 -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt
```
# To Do #
- [ ] Encrypting/signing commands to prevent unauthorized commands being issued
- [ ] Add infrastructure as code for deployment of services
- [ ] Maintain a full history of commands issued to each beacon
- [ ] Add SMB communication
- [ ] Add SMB proxying for reaching isolated VLANs
- [x] Add mTLS
