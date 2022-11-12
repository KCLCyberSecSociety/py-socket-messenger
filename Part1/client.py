''' client.py '''

from socket import *

# messenger server info
HOST = '127.0.0.1'
PORT = 50000
SERVER = (HOST, PORT)

# connects to server (client-side socket)
client = socket(AF_INET , SOCK_STREAM)
client.connect(SERVER)

print('Connected to server!')

# expects message (max 2KB) sent by server
msg_in = client.recv(2048).decode()
print('Server:', msg_in)

# sends message to server
msg_out = 'Hello Server!'
client.send(msg_out.encode())

# terminates connection with server
client.close()
