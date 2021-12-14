from gpiozero import LED
from time import sleep 
from motor import *

led = LED(4)
class TinderRobot:
    def __init__(self):
        self.right_swipes = 0
        self.left_swipes = 0
        self.matches = 0

    def swipe_right(self):
        self.right_swipes += 1
        return

    def swipe_left(self):
        self.left_swipes += 1
        return

    def return_total_swipes(self):
        return self.left_swipes + self.right_swipes

