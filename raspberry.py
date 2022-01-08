from gpiozero import OutputDevice as stepper
from time import sleep 
from motor import moveMotor

class TinderRobot:
    def __init__(self):
        self.right_swipes = 0
        self.left_swipes = 0
        self.matches = 0

        self.motorIN1 = stepper(4)
        self.motorIN2 = stepper(17)
        self.motorIN3 = stepper(27)
        self.motorIN4 = stepper(22)
        self.pins = [self.motorIN1, self.motorIN2, self.motorIN3, self.motorIN4]


    def swipe_right(self):
        self.right_swipes += 1
        moveMotor(self.pins, -370) # Extra 10 degrees because the pen hitting the phone will cause friction
        return

    def swipe_left(self):
        self.left_swipes += 1
        moveMotor(self.pins, 370)
        return

    def return_total_swipes(self):
        return self.left_swipes + self.right_swipes

