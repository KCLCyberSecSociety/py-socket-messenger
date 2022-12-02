# Part 2 - Adding SSL/TLS encryption

## Description

Now that we are able to send data across the internet, we need to add a layer of security to protect our data - otherwise, anyone with a packet-sniffer like [Wireshark](https://en.wikipedia.org/wiki/Wireshark) can view the contents of our messages. We will be using the `ssl` module to wrap our sockets with the [Transport Layer Security](https://en.wikipedia.org/wiki/Transport_Layer_Security) protocol. TLS/SSL uses encryption to verify the authenticity of our server upon connection and encrypt our messages.

## Tutorial

### Generating an SSL Certificate

An SSL certificate certifies the ownership of a public key by our server. In order to generate our SSL certificate you will require `openssl` installed on your system to generate the necessary files. Alternatively, you can use the [certificate](/Part2/certificate.pem) and [private key](/Part2/private.key) provided; the password for the private key is _password_ and is only configured for a `localhost` server

Open a terminal and run the following commands:

1. Generate an RSA private key (2048 is the number of bits in our key):

   ```bash
   openssl genrsa -aes256 -out private.key 2048
   ```

2. Convert the key from AES to RSA format

   ```bash
   openssl rsa -in private.key -out private.key
   ```

3. Create and sign a certificate using our private key authenticating our server

   ```bash
   openssl req -x509 -new -nodes -sha256 -key private.key -out certificate.pem -days 365
   ```

   When this line is run, a bunch of information is requested to generate the certificate. You can leave most fields blank, but the `Common Name` field should be `localhost`

### Server side

1. In our [server.py](/Part2/server.py) script add the following lines before creating the server socket.

   ```python
   from ssl import *

   ...

   sslctx = SSLContext(PROTOCOL_TLS_SERVER)
   sslctx.load_cert_chain('certificate.pem', 'private.key')
   ```

2. Next, we modify our socket creation by wrapping it with our SSLContext which adds the TLS layer to all our socket functions

   ```python
   server = sslctx.wrap_socket(socket(AF_INET , SOCK_STREAM), server_side=True)
   ```

### Client side

1. In our [client.py](/Part2/client.py) script, we add the following lines before creating our client socket

   ```python
   sslctx = SSLContext(PROTOCOL_TLS_CLIENT)
   sslctx.load_verify_locations('certificate.pem')
   ```

   Note: the client side only has access to the certificate. Only the server is has its private key as this can be used to decrypt our private messages. NEVER expose the private key like I have in this tutorial!

2. Change the host address from `127.0.0.1` to `localhost`. This must match our SSL certificate and cannot use the IP format

   ```python
   HOST = 'localhost'
   ```

3. Wrap the client socket with our SSLContext

   ```python
   client = sslctx.wrap_socket(socket(AF_INET , SOCK_STREAM), server_hostname=HOST)
   ```

Now if we run our scripts, the same result should occur. Although it may appear like nothing has changed, if we use Wireshark to analyze our packets, we will see additional packets (TLS handshake) and that the payload of our messages are incomprehensible i.e they have been encrypted.

## Further Reading

For more on [TLS/SSL](https://en.wikipedia.org/wiki/Transport_Layer_Security#Digital_certificates) protocol and Python's [ssl module](https://docs.python.org/3/library/ssl.html).
