''' server.py '''

from socket import *
from ssl import *

# messenger server info
HOST = 'localhost'
PORT = 50000
SERVER = (HOST, PORT)

# creates SSL contex and loads certificate and private key that signed it
sslctx = SSLContext(PROTOCOL_TLS_SERVER)
sslctx.load_cert_chain('certificate.pem', 'private.key')

# setsup server and allows clients to join (server-side socket)
server = sslctx.wrap_socket(socket(AF_INET , SOCK_STREAM), server_side=True)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(SERVER)
server.listen(1)

print('Listening for connections on port', PORT)

# creates connection with client
client, address = server.accept()
print('New client joined:', address)

# sends message to client
msg_out = 'Hello there Client!'
client.send(msg_out.encode())

# expects message (max 2KB) sent by client
msg_in = client.recv(2048).decode()
print('Client:', msg_in)

# closes connection with client and terminates server
client.close()
server.close()

