from time import sleep
# from raspberry import *
import cv2
from helper import Client


class TinderClient(Client):
    def __init__(self):
        Client.__init__(self)
    
    def send_image(self,image_location):
        # Get image size
        img = open(image_location, 'rb')
        bytes = img.read()
        size = len(bytes)
        
        # Send Image size to server
        self.sendall(("SIZE %s" % size).encode())
        answer = self.recv(4096)
        
        if answer == b"GOT SIZE":
            self.sendall(bytes)
            response = self.recv(4096)
            
            
        img.close()
        return response


client = TinderClient()
client.connect_to_server()

video_capture = cv2.VideoCapture(0)

# tinder_robot = TinderRobot()

while True:
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)

    cv2.imwrite("image.jpg", frame)
    response = client.send_image("image.jpg")
    print(response)
    sleep(3)    

    if cv2.waitKey(10) == 27: #Press the "Escape key" to terminate the program
        video_capture.release()
        cv2.destroyAllWindows()
        print("Program terminated, I hope you found your match :)")
        break
#     tinder_robot.swipe_right() if match['dominant_race'] == 'asian' else tinder_robot.swipe_left()
    