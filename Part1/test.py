import subprocess
import time
import re

class ClientError(Exception):
    pass
class ServerError(Exception):
    pass


print("Starting server...")
serverStdout = []
server = subprocess.Popen(["python", "server.py"], stdout=subprocess.PIPE)
print("Server started.")

time.sleep(0.01)

print("Starting client...")
clientStdout = []
client = subprocess.Popen(["python", "client.py"], stdout=subprocess.PIPE)

time.sleep(3)

if(server.poll() is None):
    raise ServerError("Server did not stop.")
if(client.poll() is None):
    raise ClientError("Client did not stop.")

if(server.returncode != 0):
    raise ServerError("Server Error \n:" + server.stderr.read().decode())
if(client.returncode != 0):
    raise ClientError("Client Error \n:" + client.stderr.read().decode())


serverOut = server.stdout.read().decode()
clientOut = client.stdout.read().decode()

def format_message(s):
    return re.sub(r'\s+', '', s).lower()


if(not re.match(r".*server:helloclient!*", format_message(clientOut))):
    raise ClientError("Client recieved wrong message from server: "+clientOut)
if(not re.match(r".*client:helloserver!*", format_message(serverOut))):
    raise ServerError("Server recieved wrong message from client: "+serverOut)

