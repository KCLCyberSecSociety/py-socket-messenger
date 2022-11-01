# Part 3 - Multiple clients with Multi-threading

## Description

In order to design a functioning server-client messenger, we must support sending and receiving messages from multiple client sockets simultaneously. We must also read incoming messages whilst sending a message. To perform all of these tasks concurrently, we have to use Python's `threading` module to incorporate multithreading.

We are also going to use python's `try-except-finally` clauses to properly handle connection errors. Without these, our program will crash without correctly cleaning up the network resources we allocated.

## Try-Except-Finally

Without employing `try-except-finally`, our program would crash without cleaning up the network sockets we created. A brief explanation of how these control flow structures work and are constructed:

```python
try:
  # Do something that might cause an Error
except Error1:
  # Do something in case an error of type Error1 occurs
except Error2 as err:
  # Do something using the info that might be provided by Error2
except:
  # Do something in case any type of error occurs
else:
  # Do this if an error does not occur
finally:
  # Do this regardless - even if the program exits in the above blocks
```

## Method

### Server side

In our [server.py](/Part3/server.py) script:

1. First, declare the following variables at the top to store all the client sockets that connect to our chat server and terminate our server from any thread.

    ```python
    clients = []
    running = True
    ```

2. Then create the following functions to add new client connections to our server:

    ```python
    def listen_to_client():
      # leave empty for now
      pass

    def listen_for_clients():
      try:
        while True:
          client, address = server.accept()
          
          print('New client joined: ', address)

          Thread(target=listen_to_client, args=[client, ], daemon=True).start()
          
          clients.append(client)
      except:
        running = False

3. Next, let us define the `listen_to_client` function:
    
    ```python
    def listen_to_client(client):
      try:
        while True:
          msg = client.recv(2048).decode()

          if not msg:
            break

          for c in clients:
            if c != client:
              c.send(msg.encode())
      except:
        print('Client error!')
      finally:
        client.close()

        clients.remove(client)
        
        print('Removed Client!')

        if len(clients) == 0:
            global running
            running = False
    ```

4. Now we can start listening for new clients on a daemon thread (a thread that automatically dies when the program ends)

    ```python
    Thread(target=listen_for_clients, daemon=True).start()
    ```

5. Finally, we have to wait until the running variable is set to `False` so we can end the messenger server script.

    ```python
    try:
      while running:
        pass

    except KeyboardInterrupt:
      print('Server termination requested!')
        
    except:
      print('Error, terminating server!')

    finally:
      for client in clients:
        client.close()
        
      server.close()

    print('Server has terminated!')
    ```

### Client side

In our [client.py](/Part3/client.py) script:

1. We must declare the `running` variable so that we can end the program from any thread. We will also take a username so that the client's messages can be labelled.

    ```python
    running = True
    username = input('Username: ')
    ```

2. First we edit the connection code and replace it with the following. This way we can handle a connection failure.

    ```python
    try:
      client.connect(SERVER)
    except:
      print('Failed to connect to server!')
      quit()
    else:
      print('Connected to server!')
    ```

3. Next, we define the following function to read messages sent by other clients being transferred by the server:

    ```python
    def listen_loop():
      try:
        while True:
          msg = client.recv(2048).decode()

          if not msg:
            break

          print(msg)
      except:
        print('Server error!')
        
      finally:
        global running
        running = False

        print('Connection terminated!')
    ```
  
4. We can run this method in the background by adding the following line (we set this thread as a daemon so that it will be killed when our main thread ends):

    ```python
    Thread(target=listen_loop, daemon=True).start()
    ```

5. Finally, we can allow the client to send messages to the server with the following block of code

    ```python
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
      client.close()
      print('Disconnected from server!')
    ```

## Further Reading

For an in-depth explanation of `try-catch-finally` blocks and how they are structured: [W3Schools](https://www.w3schools.com/python/python_try_except.asp). For more information on [multithreading](https://realpython.com/intro-to-python-threading/) with python. 