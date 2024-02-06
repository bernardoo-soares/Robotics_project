# Robotics_project
Robotics Lab1 2023/2024: README file -> Davide Silva, Bernardo Soares, João Castelo Branco
## How to Execute

1. **Prerequisites:**
- Python 3.0 or newer
- Internet connection (preferably not eduroam as it tends to block socket communication between computers on the same network)
   

2. **Download the Code:**
- Lab1Robot_FinalVersion -> contains the main and the respective libraries necessary to control the robots and must be used on the PC connected to the robots and the PS4 controller
- interface_robo -> contains the application that accesses the portable camera and receives information from the program running on the PC connected to the robots. It must be run on another PC.


3. **Run the interface Script:**
- The interface.zip main.py must be run on the PC connected to the portable camera.

- Its execution must be started before robot.zip's main.py (so that socket communication takes place correctly).



4. **Run the robot Script:**
- Robot.zip's main.py must be run on the PC terminal connected to the robots and the PS4 controller.

- The user must ensure that:
- Adjust the SERVER_IP in the CONSTANTS section. To check the correct value, simply use the 'ipconfig' command on the PC connected to the portable camera.
- Make sure that the COM ports associated with each robot are well defined (GLOBAL VARIABLES section).


 Note: Both scripts have usage 'messages' that are available in RUNTIME.
