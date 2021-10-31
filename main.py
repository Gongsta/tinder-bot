import time
from raspberry import *

import cv2
from deepface import DeepFace


video_capture = cv2.VideoCapture(0)

ret, frame = video_capture.read()
cv2.imshow('Video', frame)
time.sleep(1)

while True:
    ret, frame = video_capture.read()
    cv2.imshow('Video', frame)

    cv2.imwrite("image.jpg", frame)
    # actions = ['age', 'gender', 'race', 'emotion']
    try:
        match = DeepFace.analyze(img_path = "image.jpg", actions = ['race'])
        print(match)

        swipe_right() if match['race'] == 'Asian' else swipe_left()

    except:
        print("Face could not be detected")
        swipe_left()


    if cv2.waitKey(10) == 27: #Press the "Escape key" to terminate the program
        video_capture.release()
        cv2.destroyAllWindows()
        print("Program terminated, I hope you found your match :)")
        break