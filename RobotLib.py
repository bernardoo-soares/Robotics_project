import serial
import time
from ps4ControllerLib import *
import numpy as np
import math
import re

# Important constants
ROBOT_DISTANCE = 0.9 # Distance between the robots bases
WAIT = 0.5

# Functions to set robots and serial coomunication

def setPort(port):
    # Open the serial port COM to communicate with the robot 
    ser = serial.Serial(port, baudrate=9600, bytesize=8, timeout=2, parity='N', xonxoff=0, stopbits=serial.STOPBITS_ONE)
    return ser

def setRobot(ser):

    # This function sets the robot connected though the serial port 'ser'
    # in the desired configuration. 

    # Clear input and output buffers
    ser.flushInput()
    ser.flushOutput()


    # Turn off the manual mode
    sendCommand(ser, '~')    
    serString = receiveCommand(ser, WAIT)
    
    if not("EXIT MANUAL MODE" in serString): #Make sure it exits manual mode
        sendCommand(ser, '~')
        serString = receiveCommand(ser, WAIT)

    # Set the speed to 50
    sendCommand(ser, 'SPEED 50')
    serString = receiveCommand(ser, WAIT)

    # Turn on manual mode again
    sendCommand(ser, '~')
    serString = receiveCommand(ser, WAIT)
    
    # Turning on the Controls
    sendCommand(ser, 'C')
    serString = receiveCommand(ser, WAIT)

    # Setting XYZ mode
    sendCommand(ser, 'X')
    serString = receiveCommand(ser, WAIT)




# Functions to send and receive commands to the robot

def sendCommand(ser, command):
    # This function sends a command to the robot (receiveCommand should be used to wait for a response)
    ser.write(command.encode("Ascii") + b'\r')
    ser.flush()

def receiveCommand(ser, timeout):
    # This function receives a command from the robot and waits for a response
    # It returns the string of characters

    output = ""
    flag = True
    start_time = time.time()

    while flag:
        # Wait until there is data waiting in the serial buffer
        if ser.in_waiting > 0:
            # Read data out of the buffer until a carriage return / new line is found
            serString = ser.readline()
           
            try:
                output += serString.decode("Ascii")
                
            except:
                print("-> Error decoding character!") 
        
        
        else:
            deltat = time.time() - start_time

            if deltat>timeout:
                flag = False # Break if timeout is reached

    if output == "":
        print("-> No received data!")

    # Clear input buffer
    ser.flushInput()
        
    # Return the received string
    return output



# Functions to compute the correct movement command to be sent to the robot
  
def computeMoveCommand(ser, joystick, robot, mode):

    if mode: ######################################### XYZ mode ############################################3

        # Check the state of the joysticks and d-pad
        x_value = joystick.get_axis(LEFT_ANALOG_HORIZONTAL)
        y_value = joystick.get_axis(LEFT_ANALOG_VERTICAL)
        z_value = [joystick.get_button(UP_ARROW), joystick.get_button(DOWN_ARROW)]
        
        pitch_value = joystick.get_axis(RIGHT_ANALOG_HORIZONTAL)
        roll_value = joystick.get_axis(RIGHT_ANALOG_VERTICAL)

        if robot == 1: #  ****************** CAMERA ROBOT ******************
            # AXIS X (horizontal left joystick) 
            if abs(y_value) > JOYSTICK_THRESHOLD:
                if y_value > 0:
                    sendCommand(ser, 'Q')
                else:
                    sendCommand(ser, '1')

            # AXIS Y (vertical left joystick)
            if abs(x_value) > JOYSTICK_THRESHOLD:    
                if x_value > 0:
                    sendCommand(ser, 'W')
                else:
                    sendCommand(ser, '2')

            # AXIS Z (Arrows) 
            if z_value[1] > 0:  # Up arrow
                sendCommand(ser, 'E')  
            elif z_value[0] > 0:  # Down arrow
                sendCommand(ser, '3')
        
            # PITCH (right horizontal joystick)
            if abs(pitch_value) > JOYSTICK_THRESHOLD:
                if pitch_value > 0:
                    sendCommand(ser, '5')  # Pitch in one direction
                else:
                    sendCommand(ser, 'T')

            # ROLL (right vertical joystick)
            if abs(roll_value) > JOYSTICK_THRESHOLD:
                if roll_value > 0:
                    sendCommand(ser, '4') # Roll in one direction
                else:
                    sendCommand(ser, 'R')


        else: # ****************** BISTOURI ROBOT ******************

            # AXIS X (horizontal left joystick) 
            if abs(y_value) > JOYSTICK_THRESHOLD:
                if y_value > 0:
                    sendCommand(ser, '1')
                else:
                    sendCommand(ser, 'Q')

            # AXIS Y (vertical left joystick)
            if abs(x_value) > JOYSTICK_THRESHOLD:    
                if x_value > 0:
                    sendCommand(ser, '2')
                else:
                    sendCommand(ser, 'W')

            # AXIS Z (Arrows) 
            if z_value[1] > 0:  # Up arrow
                sendCommand(ser, 'E')  
            elif z_value[0] > 0:  # Down arrow
                sendCommand(ser, '3')
        
            # PITCH (right horizontal joystick)
            if abs(pitch_value) > JOYSTICK_THRESHOLD:
                if pitch_value > 0:
                    sendCommand(ser, '5')  # Pitch in one direction
                else:
                    sendCommand(ser, 'T')

            # ROLL (right vertical joystick)
            if abs(roll_value) > JOYSTICK_THRESHOLD:
                if roll_value > 0:
                    sendCommand(ser, '4') # Roll in one direction
                else:
                    sendCommand(ser, 'R')




    else: ###################################### Joint mode ###############################################
            
            # Check the state of the joysticks and d-pad
            shoulder = joystick.get_axis(LEFT_ANALOG_HORIZONTAL)
            base = joystick.get_axis(LEFT_ANALOG_VERTICAL)
            elbow = [joystick.get_button(UP_ARROW), joystick.get_button(DOWN_ARROW)]
            
            pitch_value = joystick.get_axis(RIGHT_ANALOG_HORIZONTAL)
            roll_value = joystick.get_axis(RIGHT_ANALOG_VERTICAL)

            if robot == 1: #****************** CAMERA ROBOT ******************
                # BASE (horizontal left joystick) 
                if abs(base) > JOYSTICK_THRESHOLD:
                    if base > 0:
                        sendCommand(ser, 'W')
                    else:
                        sendCommand(ser, '2')


                # SHOULDER (vertical left joystick)
                if abs(shoulder) > JOYSTICK_THRESHOLD:    
                    if shoulder > 0:
                        sendCommand(ser, '1')
                    else:
                        sendCommand(ser, 'Q')

                # ELBOW (Arrows)
                if elbow[1] > 0:  # Up arrow
                    sendCommand(ser, 'E')  
                elif elbow[0] > 0:  # Down arrow
                    sendCommand(ser, '3')


            else: # B****************** BISTOURI ROBOT ******************
                # BASE (horizontal left joystick)
                if abs(base) > JOYSTICK_THRESHOLD:    
                    if base > 0:
                        sendCommand(ser, 'W')
                    else:
                        sendCommand(ser, '2')

                # SHOULDER (vertical left joystick)
                if abs(shoulder) > JOYSTICK_THRESHOLD:    
                    if shoulder > 0:
                        sendCommand(ser, '1')
                    else:
                        sendCommand(ser, 'Q')

                # ELBOW (Arrows)
                if elbow[1] > 0:  # Up arrow
                    sendCommand(ser, 'E')  
                elif elbow[0] > 0:  # Down arrow
                    sendCommand(ser, '3')


                # PITCH (right horizontal joystick)
                if abs(pitch_value) > JOYSTICK_THRESHOLD:
                    if pitch_value > 0:
                        sendCommand(ser, '5')  # Pitch in one direction
                    else:
                        sendCommand(ser, 'T')

                # ROLL (right vertical joystick)
                if abs(roll_value) > JOYSTICK_THRESHOLD:
                    if roll_value > 0:
                        sendCommand(ser, 'R') # Roll in one direction
                    else:
                        sendCommand(ser, '4')
    


# Functions to get parameters from the robot

def getRobotSpeed(ser):
    # This function returns the current speed of the robot
    sendCommand(ser, 'SHOW SPEED')
    serString = receiveCommand(ser, 0.2)

    # Extract the speed from the string as an integer
    speed = re.findall(r'\d+', serString)[0]
    speed = int(speed)

    return speed