''' client.py '''

from socket import *
from ssl import *

# messenger server info
HOST = 'localhost'
PORT = 50000
SERVER = (HOST, PORT)

# creates SSL contex and loads server's certificate
sslctx = SSLContext(PROTOCOL_TLS_CLIENT)
sslctx.load_verify_locations('certificate.pem')

# connects to server (client-side socket)
client = sslctx.wrap_socket(socket(), server_hostname=HOST)
client.connect(SERVER)

print('Connected to server')

# reads message sent by server
msg_in = client.recv(1024).decode()
print('Server:', msg_in)

# sends message to server
msg_out = 'Hello Server!'
client.send(msg_out.encode())

# terminates connection with server
client.close()

