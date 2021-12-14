# tinder-bot
This is a simple tinder robot project I used to automate the process of swiping on tinder. The project includes non-discriminatory racial detection with the use of the Deepface Python library, and swipes right on  Asians.

At first, I tried to host all of the code on the Raspberry Pi, but ran into several errors due to the limited computing power of this tiny computer. Thus, in the end the Raspberry Pi acts as a simple client, that sends pictures through its Raspberry Pi to the server.

Then, the server takes that image, processes it and returns a message. The robot then takes that response, and turns a motor to either swipe right or left if it is asian.
