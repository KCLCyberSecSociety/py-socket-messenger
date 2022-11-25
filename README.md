# Python TCP Client-Server Socket Messenger

## Description

This tutorial will show you how to write a simple TCP socket client-server messenger in Python3 using python's standard `socket` module. We will use the `ssl` module to provide TLS to encrypt our messages securing our connection from malicious actors.

[Slides](https://docs.google.com/presentation/d/1FUudkuJAo3W2TyuWn0hX-wBt_I_TwvV1)

## Prerequisites

To follow along with this tutorial:

- [Python](https://www.python.org/downloads/) version 3 or higher is required, including the command line tools so that we can execute python from our terminal.

- For Part2, having [OpenSSL](https://www.openssl.org/) installed on you system would be beneficial, however, you can use the keys and certificates provided.

- A code editor would also come in quite handy; you can use Python IDLE or Visual studio code or even notepad.

## Navigation

To commence this tutorial, navigate to the code section of this repository, enter the `PartX` subdirectory. This tutorial is divided into three parts, each part available as a separate subdirectory. Then just follow the `README.md`

### Contents

- [Part 1](/Part1) - TCP connection, data transfer, shutdown

- [Part 2](/Part2) - Secure with SSL/TLS

- [Part 3](/Part3) - Multiple clients, multi-threading, error handling

## Notes

The RSA private key and SSL certificate generated for Part2 is purely for demonstration purposes. You should NEVER expose private keys by storing them on a public (or even private) repository. So it would be ill-advised to reuse the keys I have provided for any personal project.
