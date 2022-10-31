''' server.py '''

from socket import *

# Messenger server info
HOST = '127.0.0.1'
PORT = 50000
SERVER = (HOST, PORT)

# setsup server and allows clients to join (server-side socket)
server = socket()
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(SERVER)
server.listen(1)

print('Listening for connections on port ', PORT)

# creates connection with client
client, address = server.accept()
print('New client joined:', address)

# sends message to client
msg_out = 'Hello client!'
client.send(msg_out.encode())

# expects message (max 2KB) sent by client
msg_in = client.recv(2048).decode()
print('Client:', msg_in)

# closes connection with client and terminates server
client.close()
server.close()
