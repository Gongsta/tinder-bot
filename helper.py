"""
Jun Yu Gong, 1931135
Wednesday, April 28th
R. Vincent , instructor
Final Project
"""

import socket
import threading
import pickle #used for serialization (converting objects to bytes) of objects and transfer them over networks
import json #similar to pickle
import time #used for timeouts

class Server(socket.socket):
    """
    A Server class built on top of the socket.socket class. It waits for incoming requests

    Several functions have been added to make the process of setting up a server easier.
    """
    def __init__(self, PORT=5050, HOST_NAME=socket.gethostname(), FORMAT='utf-8', DISCONNECT_MESSAGE = "!disconnect", HEADER_LENGTH = 64):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM) #Create a socket with family AF_INET (ipv4) and type SOCK_STREAM (TCP socket)

        self.PORT = PORT #Define the port number
        self.HOST_NAME = HOST_NAME #Define the host name
        self.IP = socket.gethostbyname(self.HOST_NAME) #IPV4 address
        self.FORMAT = FORMAT #Default is utf-8
        self.DISCONNECT_MESSAGE = DISCONNECT_MESSAGE #Message to disconnect client from server
        self.HEADER_LENGTH = HEADER_LENGTH #Headers are used used to inform the length of the message

        self.USE_TIMEOUT = False #Depending on the application, timeouts can be useful to alleviate the server of multiple connections
        self.TIMEOUT = 60 #default timeout of 60 seconds


        self.connections = [] #List of connections
        self.addresses = [] #List of addresses

        self.bind((self.HOST_NAME, self.PORT))

    def handle_client(self, connection, address):
        """
        Handle a client connection.
        """
        print(f"[NEW CONNECTION] {address} connected.")

        connected = True #State for whenever a client connects
        most_recent_call = time.time() #Variable to keep track of timeouts
        #TODO: Timeouts
        while connected: #Loop that continuously runs for the server to actively listen to client requests

            encoded_message_length = connection.recv(self.HEADER_LENGTH)
            message_length = encoded_message_length[:self.HEADER_LENGTH].decode("utf-8")

            if message_length: #Only run the following code if the message is not empty
                most_recent_call = time.time()
                message_length = int(message_length)
                message = connection.recv(message_length)

                #TODO: Implement hash table to ensure that data is not lost


                connected = False if message == self.DISCONNECT_MESSAGE else True #Disconnect client if disconnect message is sent

                self.handle_client_message(message, address, connection)

            if self.USE_TIMEOUT and time.time() - most_recent_call > self.TIMEOUT: #If the timeout has been exceed, then disconnect the client. Default to False
                connected = False


        connection.close()
        self.connections.remove(connection)
        self.addresses.remove(address)
        print(f"[CONNECTION CLOSED] {address} disconnected.")

    def handle_client_message(self, message, address, connection):

        if self.FORMAT == "pickle":  # Handle pickle object
            decoded_message = pickle.loads(message)  # decode pickle object

        elif self.FORMAT == "JSON":  # TODO: Implement JSON Handling
            decoded_message = json.loads(message)  # decode json object

        elif self.FORMAT == "utf-8":  # Handle message as a string
            decoded_message = message.decode("utf-8")  # Header will give us the length of the message

        """Can be overridden depending on the application. Function that handles what to do with the message given by the client after it has been decoded"""
        print(f"[MESSAGE FROM {address}] {decoded_message}")
        connection.send("Message received".encode("utf-8"))


    def start(self):
        """Start the server. """
        self.listen() #Listen for incoming connections
        print(f"[LISTENING] Server is listening on {self.IP}")
        while True: #Start infinite loop

            connection, address = self.accept()
            self.connections.append(connection)
            self.addresses.append(address)
            thread = threading.Thread(target=self.handle_client, args=(connection, address)) #Threading allows the server to handle multiple incoming connections
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

            #TODO: Control-C Implementation https://stackoverflow.com/questions/3788208/threading-ignores-keyboardinterrupt-exception




class Client(socket.socket):
    """Clients send requests to servers. """
    def __init__(self, PORT=5050, HOST_NAME=socket.gethostname(), FORMAT='utf-8', HEADER_LENGTH=64):
        socket.socket.__init__(self, socket.AF_INET, socket.SOCK_STREAM) #Create a socket with family AF_INET (ipv4) and type SOCK_STREAM (TCP socket)

        self.PORT = PORT #Define the port number
        self.HOST_NAME = HOST_NAME #Defin the post name
        self.FORMAT = FORMAT #Default is utf-8
        self.HEADER_LENGTH = HEADER_LENGTH #Headers are used used to inform the listener the length of the message

    def connect_to_server(self):
        self.connect((self.HOST_NAME, self.PORT)) #connect to server
        print(f"[CONNECTED] Client connected to {self.HOST_NAME}")

    def send_message(self, initial_message):
        if self.FORMAT == "pickle":
            encoded_message = pickle.dumps(initial_message) #Convert the message object to a byte string

        elif self.FORMAT == "JSON": #TODO: Test JSON Implementation
            encoded_message = json.dumps(initial_message)

        elif self.FORMAT == "utf-8":
            encoded_message = initial_message.encode("utf-8") #Encode message in utf-8

        message_length = len(encoded_message)
        final_encoded_message = f"{message_length:<{self.HEADER_LENGTH}}".encode("utf-8") + encoded_message #Add encoded header to original message
        self.send(final_encoded_message) #send message to server
        if initial_message == "!disconnect":
            self.close()

        # print(f"[MESSAGE SENT] {message}")
        # print(f"[CONFIRMATION MESSAGE FROM SERVER] {self.recv(2048).decode('utf-8')}") #Print out confirmation message


