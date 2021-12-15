import time

from deepface import DeepFace
from helper import Server
import json

class TinderServer(Server):
    def __init__(self):
        Server.__init__(self)
        self.img_counter = 1
        self.img_basename = "./images/image%s.jpg"
        try:
            f = open('data.json')
            self.match_data = json.load(f)
        except:
            self.match_data = []


    def handle_client(self, connection, address):
        """
        Handle a client connection.
        """
        print(f"[NEW CONNECTION] {address} connected.")

        connected = True #State for whenever a client connects
        most_recent_call = time.time() #Variable to keep track of timeouts

        while connected: #Loop that continuously runs for the server to actively listen to client requests

            encoded_message_length = connection.recv(self.HEADER_LENGTH)
            data = encoded_message_length[:self.HEADER_LENGTH]

            if data: #Only run the following code if the message is not empty
                most_recent_call = time.time()
                connected = False if data == self.DISCONNECT_MESSAGE else True #Disconnect client if disconnect message is sent
                
                if data.startswith(b"SIZE"):
                    tmp = data.split()
                    size = int(tmp[1])
                    print("Receiving image with size", size)
                    connection.send("GOT SIZE".encode())
                
                else:
                    self.handle_client_image(data, address, connection)



            if self.USE_TIMEOUT and time.time() - most_recent_call > self.TIMEOUT: #If the timeout has been exceed, then disconnect the client. Default to False
                connected = False


        connection.close()
        self.connections.remove(connection)
        self.addresses.remove(address)
        print(f"[CONNECTION CLOSED] {address} disconnected.")


    def handle_client_image(self, data, address, connection):
        myfile = open(self.img_basename % self.img_counter, 'wb')
        myfile.write(data)
        
        data = connection.recv(40960000)
        if not data:
            myfile.close()
        
        myfile.write(data)
        myfile.close()
        
        match = self.process_image(self.img_basename % self.img_counter)
        if match:
            connection.send("Asian".encode())
        else:
            connection.send("Not Asian".encode())
        self.img_counter += 1
    
    def process_image(self, image_path):
        try:
            match = DeepFace.analyze(img_path = image_path, actions = ['race'])
            self.match_data.append(match)
            self.write_data_to_json(self.match_data)
            if match['dominant_race'] == 'asian':
                return True

        except Exception as e:
            print(e)
            return False

        return False
    def write_data_to_json(self, match):
        # Hard store this data that can be analyzed at a later time
        # TODO:
        with open("data.json", "w") as f:
            json.dump(self.match_data, f)

server = TinderServer()
server.start()

    
