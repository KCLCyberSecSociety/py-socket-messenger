# client

from ssl import *
from socket import *
from threading import *

# client will run until this is set to False
running = True

username = input('Username: ')

# messenger server info 
HOST = 'localhost'
PORT = 50000
SERVER = (HOST, PORT)

# setsup SSL context
sslctx = SSLContext(PROTOCOL_TLS_CLIENT)
sslctx.load_verify_locations('certificate.pem')

# setsup connection to server
client = sslctx.wrap_socket(socket(), server_hostname=HOST)

# connects to server properly
try:
    client.connect(SERVER)
except:
    print('Failed to connect to server!')
    quit()
else:
    print('Connected to server!')


def listen_loop():
    '''Listens for messages sent by server and prints them until the connection
    is closed by the server or by this client. '''
    try:
        while True:
            msg = client.recv(2048).decode()

            # stop listening when server closes connection
            if not msg:
                break

            print(msg)
    except:
        print('Server error!')
        
    finally:
        global running
        running = False

        print('Connection terminated!')


# starts listening to the server until connection is closed
Thread(target=listen_loop, daemon=True).start()

# sends messages to server until the connection is closed
try:
    while running:
        msg = input('')

        if msg == 'exit':
            running = False
        else:
            msg = '[' + username + '] ' + msg
            client.send(msg.encode())
except:
    print('Failed to send message')

finally:
    # closes connection to server
    client.close()

    print('Disconnected from server!')

