# server

from ssl import *
from socket import *
from threading import *

# stores all client connections (sockets)
clients = []

# server will run until this is set to False
running = True

# messenger server info 
HOST = 'localhost'
PORT = 50000
SERVER = (HOST, PORT)

# setsup SSL context
sslctx = SSLContext(PROTOCOL_TLS_SERVER)
sslctx.load_cert_chain('certificate.pem', 'private.key')

# setsup server and allows client to join (server-side socket)
server = sslctx.wrap_socket(socket(AF_INET , SOCK_STREAM), server_side=True)
server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
server.bind(SERVER)
server.listen(5)

print('Listening for connections on port ', PORT)


def listen_to_client(client):
    '''This function listens to messages sent to the server by a client and
    forwards the message to all other clients connected to the server. When
    the client closes the connection, they are removed from the server. '''

    try:
        while True:
            msg = client.recv(2048).decode()

            # stop listening to client when client closes connection
            if not msg:
                break

            # sends message to all other connected clients
            for c in clients:
                if c != client:
                    c.send(msg.encode())
    except:
        print('Client error!')
    
    finally:
        # terminate client connection and remove them from connected clients list
        client.close()

        clients.remove(client)
        
        print('Removed Client!')

        # close server if no clients are left
        if len(clients) == 0:
            global running
            running = False


def listen_for_clients():
    '''This function listens for new clients trying to connect to the server
    and starts listening for messages sent by them on a new thread. '''
    try:
        while True:
            client, address = server.accept()
            
            print('New client joined: ', address)

            # listens for incoming messages from client on different thread
            Thread(target=listen_to_client, args=[client, ], daemon=True).start()
            
            clients.append(client)
    except:
        running = False

# starts listening for new connections on new thread
Thread(target=listen_for_clients, daemon=True).start()

try:
    # wait here until server has been stopped (running=False)
    while running:
        pass

# allows user to close server by pressing 'Ctrl-C'
except KeyboardInterrupt:
    print('Server termination requested!')
    
except:
    print('Error, terminating server!')

finally:
    # closes all client connections
    for client in clients:
        client.close()

    # closes server socket
    server.close()

    print('Server has terminated!')

