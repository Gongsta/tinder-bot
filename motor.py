from gpiozero import OutputDevice as stepper
from time import sleep


xAxisMotorIN1 = stepper(4)
xAxisMotorIN2 = stepper(17)
xAxisMotorIN3 = stepper(27)
xAxisMotorIN4 = stepper(22)

xAxisPins = [xAxisMotorIN1, xAxisMotorIN2, xAxisMotorIN3, xAxisMotorIN4]


def moveMotor(angle=180, mode="SPEED", pins=xAxisPins, stepsPerRevolution = 2048):
  stepsToComplete = int(angle * stepsPerRevolution / 360)

  # https://www.hackster.io/mjrobot/playing-with-electronics-rpi-gpio-zero-library-tutorial-f984c9#toc-controlling-a-stepper-motor-6
  if mode == "POWER": #The angle with the power mode is not right, TODO
    seq = [[1,0,0,1], # Define step sequence as shown in manufacturers datasheet
              [1,0,0,0], 
              [1,1,0,0],
              [0,1,0,0],
              [0,1,1,0],
              [0,0,1,0],
              [0,0,1,1],
              [0,0,0,1]]
  elif mode == "SPEED":                    # High Speed ==> Low Power 
    seq = [[1,0,0,0], # Define step sequence as shown in manufacturers datasheet
              [0,1,0,0],
              [0,0,1,0],
              [0,0,0,1]]

  # If turn clockwise, stepDir is positive
  if (stepsToComplete < 0):
    stepDir = -1 
  else:
    stepDir = 1 
  
  seqCount = len(seq)
  waitTime = 0.002 
  stepCounter = 0
  seqCounter = 0

  while True:
    print(seqCounter)
    for i in range(4):
      pin = pins[i]
      if seq[seqCounter][i] != 0:
        pin.on()
      else:
        pin.off()
      
    seqCounter += stepDir
    if (abs(seqCounter ) >= seqCount):
      seqCounter = 0

    stepCounter += stepDir   
    #if stepCounter == stepsToComplete:
     # break

    sleep(waitTime)

moveMotor()
sleep(2)
moveMotor(-90.1)
