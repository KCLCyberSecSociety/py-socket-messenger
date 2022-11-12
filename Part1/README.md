# Part 1 - Creating a TCP server-client Connection

## Description

First, we will have to create a [client](/Part1/client.py) and [server](/Part1/server.py) script which will be run simultaneously. TCP sockets can be accessed using the `socket` module and we will test our scripts using a localhost/loopback connection.

## Tutorial

### Server side

1. First, in [server.py](/Part1/server.py), write the following code to import all resources from the `socket` module and store the localhost server info.

    Here, I've used port `5000`, which will probably not be used by another program or process, however, if you notice the server is taking a long time to connect, change the port number.

    ```python
    from socket import *

    HOST = '127.0.0.1'
    PORT = 50000
    SERVER = (HOST, PORT)
    ```

2. Next, we create the server socket like so:
    
    ```python
    server = socket(AF_INET , SOCK_STREAM)
    ```
    + We specify the address family to `AF_INET` to allow IPv4 addresses to connect to it. 
    + We specify the socket type to `SOCK_STREAM` to ensure a continuous connection is maintained.
    
    ```python
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    ```
    We want to configure the socket so that the same socket `host:port` can be used again. The method `setsockopt` targets the socket option level to `SOL_SOCKET`, we specify that we want to set the socket option `SO_REUSEADDR` to `1` i.e `true` 

    For more info on: [setsockopt](https://pubs.opengroup.org/onlinepubs/000095399/functions/setsockopt.html)

    ```python
    server.bind(SERVER)
    server.listen(1)
    ```
    Finally, we establish the socket on our system using the `bind` method and begin listening for incoming connections using `listen`. The `listen` method takes in a number specifying the number of connections that wait to connect before denying any more.

3. Then, we want to allow a connection to be established:

    ```python
    client, address = server.accept()
    print('New client joined:', address)
    ```
    The `accept` method returns the `address` and the `socket` of the person who connected with the server - this can be used to send data to the new client.

    The `accept` method is a blocking function i.e the program is stuck here until a connection is made.

4. Now that a connection has been established, we can send a message to the client like so:

    ```python
    msg_out = 'Hello client!'
    client.send(msg_out.encode())
    ```

    The `encode` function that we call on the string converts it into `bytes` which can be transmitted over our TCP connection

5. We can also receive messages like so:

    ```python
    msg_in = client.recv(2048).decode()
    print('Client:', msg_in)
    ```
    The `recv` method is used to receive data from the client - the method requires the number of bytes that are expected to be received. This is also a blocking function.

6. Finally, we must terminate the server by closing the client and server sockets

    ```python
    client.close()
    server.close()
    ```

### Client side

1. Next, in [client.py](/Part1/client.py), we are going to develop the client script to connect to our server. We reuse this code from the server script as we're connecting to the same location.

    ```python
    from socket import *

    HOST = '127.0.0.1'
    PORT = 50000
    SERVER = (HOST, PORT)
    ```

2. This time, in order to connect to our server we use the `connect` method.

    ```python
    client = socket(AF_INET , SOCK_STREAM)
    client.connect(SERVER)
    ```
    DO NOT confuse this method with `bind` as it can only be used to initiate a server-side socket for clients to `connect` to.

3. Again, we can receive and send messages in the same fashion

    ```python
    msg_in = client.recv(2048).decode()
    print('Server:', msg_in)

    msg_out = 'Hello Server!'
    client.send(msg_out.encode())
    ```

4. Finally we close the connection like so:

    ```python
    client.close()
    ```

### Running
Open two separate terminals and execute the following commands:

1. First, in terminal 1

    ```bash
    python server.py 
    ```

2. Then, in terminal 2

    ```bash
    python client.py 
    ```

## Further Reading

For more information on python socket programming, you can refer to the official documentation for the [socket](https://docs.python.org/3/library/socket.html) module.

For more information on the TCP protocol, please refer to: [Transmission Control Protocol](https://en.wikipedia.org/wiki/Transmission_Control_Protocol)