# Robotics 23-24, Lab1 serial communications with the Scorbot example

# Import libraries
import RobotLib as R
import time
import pygame
import os
from ps4ControllerLib import *

# Important constants
SLEEP = 0.005 
WAIT = 0.1


def main():

    # Clear the terminal
    os.system('cls')
    print("\n\nStarting...")

    # Initialize Pygame and joystick (we asssume there is only one joystick connected)
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    
    # Open the serial ports to communicate with the robots (change to valid port)
    ser1 = R.setPort('COM4')
    ser2 = R.setPort('COM5')

    # Homing the robots (only in first run of the day)
    ser1.write(b'home\r')
    ser2.write(b'home\r')
    time.sleep(180) # homing takes a few minutes ...

    # Set the robots
    R.setRobot(ser1) # camera robot
    print("Camera robot set...")
    R.setRobot(ser2) # bistouri robot
    print("Bistouri robot set...")

    # Initialize the controlled robot (should be the camera first)
    ser = ser1

    # Variables that indicate the controlled mode
    modeXYZ = True
    robot1 = True # True if the camera robot is being controlled

    # Send information to the user computer
    pass
    
    # Main loop
    running = True
    while running:

        # 1 - Process event queue
        pygame.event.pump()  

        # 2 - Check for digital button press events to perform discrete actions
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:

                # Exit the program by clicking the PS button
                if event.button == PS: 
                    running = False
                    break
                
                #Change the controlled robot by pressing the Share button
                if event.button == SHARE:
                    if ser == ser1:
                        robot1 = False
                        ser = ser2
                    else:
                        robot1 = True
                        ser = ser1

                # Change from XYZ to Joint mode (and vice versa) by clicking the Options button
                if event.button == OPTIONS:
                    if modeXYZ:
                        modeXYZ = False
                        R.sendCommand(ser, 'J')
                        R.receiveCommand(ser, WAIT)
                    else:
                        modeXYZ = True
                        R.sendCommand(ser, 'X')
                        R.receiveCommand(ser, WAIT)

                # Increase speed in 10%
                if event.button == RIGHT_ARROW:

                    current_speed = R.getRobotSpeed(ser)
                    new_speed = current_speed + 10
                    if new_speed > 100:
                        new_speed = 100

                    R.sendCommand(ser, 'SPEED ' + str(new_speed))
                    R.receiveCommand(ser, WAIT)

                # Decrease speed in 10%
                if event.button == LEFT_ARROW:

                    current_speed = R.getRobotSpeed(ser)
                    new_speed = current_speed - 10
                    if new_speed < 10:
                        new_speed = 10
                    
                    R.sendCommand(ser, 'SPEED ' + str(new_speed))
                    R.receiveCommand(ser, WAIT)

                # Save current position
                if event.button == X:

                    R.sendCommand(ser, 'HERE pos1')
                    R.receiveCommand(ser, WAIT)

                # Go to last saved position
                if event.button == TRIANGLE:
                    R.sendCommand(ser, 'MOVE pos1')
                    R.receiveCommand(ser, WAIT)


            pass # Send information to the user related to this
                
        # 3 - Check for running condition
        if not running:
            break

        # 4 - Select a valid MOVEMENT command to send to the robot (perform continuous actions)
        R.computeMoveCommand(ser, joystick, robot1, modeXYZ)

        # 5 - Delay and continue while loop
        time.sleep(SLEEP)

        

    # Close the serial connection and pygame
    ser.close()
    pygame.quit()

    # Finish program
    os.system('cls')
    print('\n\nDISCONNECTED... THANK YOU FOR PLAYING\n\n')
    return 0



########################################################################
if __name__ == "__main__":
    main()