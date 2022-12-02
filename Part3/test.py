import subprocess
import time
import re


class ClientError(Exception):
    pass


class ServerError(Exception):
    pass


def format_message(s):
    return re.sub(r'\s+', '', s).lower()


print("Starting server...")

server = subprocess.Popen(["python", "server.py"], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True)
print("Server started.")

time.sleep(0.01)


print("Starting clients ...")
client1 = subprocess.Popen(["python", "client.py"],  stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
client2 = subprocess.Popen(["python", "client.py"],  stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

time.sleep(0.5)


# Write username
client1.stdin.write("Client1\n")
client1.stdin.flush()
client2.stdin.write("Client2\n")
client2.stdin.flush()


time.sleep(0.5)

client1.stdin.write("Hello Client 2\n")
client1.stdin.flush()


time.sleep(0.5)

client2.stdin.write("Hello Client 1\n")
client2.stdin.flush()


time.sleep(0.5)

client1.kill()
client2.kill()


c2recieved = client2.stdout.read()


if (not re.match(r".*helloclient2.*", format_message(c2recieved))):
    raise ClientError("Client2 recieved: " + c2recieved)

print("Test passed")
