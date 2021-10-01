# Import socket module
from socket import *
import requests

# create a cache
cache = []


# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)

# Defining serverSocket HOST and PORT, and listening
HOST = '127.0.0.1'
PORT = 32007
serverSocket.bind((HOST, PORT))
serverSocket.listen()

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')

    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()  # Fill in start             #Fill in end

    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024)  # Fill in start           #Fill in end

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        url = "http:/" + message.split()[1].decode()

        cached = False
        # Check if the url is cached
        for entry in cache:
            if url == entry[0]:
                cached = True
                outputdata = entry[1]
                print("returned from cache")

        if not cached:
            # Because the extracted path of the HTTP request includes
            # a character '\', we read the path from the second character
            f = requests.get(url)

            # Store the entire content of the requested file in a temporary buffer
            outputdata = f.text

            # add data to cache
            cache.append((url, outputdata))

        # Send the HTTP response header line to the connection socket
        # Fill in start
        # Connection is successful if it gets here
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        # Fill in end

        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.send("\r\n".encode())

        # Close the client connection socket
        connectionSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        # Fill in start
        connectionSocket.send("HTTP/1.1 404 Not found\r\n\r\n".encode())
        # Fill in end

        # Close the client connection socket
        # Fill in start
        connectionSocket.close()
    # Fill in end

serverSocket.close()
