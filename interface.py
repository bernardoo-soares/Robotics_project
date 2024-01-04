import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import threading
import socketLib as s
    

# Initial values for the robot state
robot_state = {

    'Robot': "Camera",
    'Mode': "Joint",
    'Speed': "50",

}


# Path to images
modo_imagem = {
    ('Camera', 'X'): 'c:/Users/berna/OneDrive/Lab1Rob_11_12_fim1111/Robot1_xyz.png',
    ('Camera', 'J'): 'c:/Users/berna/OneDrive/Lab1Rob_11_12_fim1111/Robot1_joint.png',
    ('Bistouri', 'X'): 'c:/Users/berna/OneDrive/Lab1Rob_11_12_fim1111/Robot1_xyz.png',
    ('Bistouri', 'J'): 'c:/Users/berna/OneDrive/Lab1Rob_11_12_fim1111/Robot1_joint.png',
}



class CameraApp(tk.Tk):

    def __init__(self, window_title="Interface"):

        super().__init__()
        self.title(window_title)
        self.attributes("-fullscreen", True)
        self.configure(background="Black")

        self.cap = cv2.VideoCapture(0)
    

        # Variable to track interface state
        self.full_screen_camera = False

        self.initial_interface()
        
        # Initial state of the right frame, use the information from the server to set this value



    def initial_interface(self):
        
        
        self.initial_label = tk.Label(self, text="Robots are configuring, please wait a few minutes...",
                                    fg="white", bg="black", font=("Comic Sans MS", 33, "bold"))
        
        self.initial_label.pack(expand=True)

        
        self.after(5000, self.setup_main_interface)  # Simulate a 5-second configuration time



    def setup_main_interface(self): 


        # Destroy the initial frame
        self.initial_label.destroy()
        
        print("Setting up main interface...")

        # Set the server
        self.server, self.client_socket = s.setServer(s.SERVER_IP, s.SERVER_PORT)
        
        flag = s.waitForUpdate(self.client_socket)

        if flag == "Start":
            
            # Start the thread to fetch robot state
            thread = threading.Thread(target=self.change_robot_state, daemon=True)
            
            thread.start()


            # Colors settings 
            self.greycolor = "#f3f4f6"  # Light grey color (fundo)
            self.text_color = "#333333"  # Dark grey color for text for readability
            self.titles_color = "#2a9d8f"  # color for headings

            # Divide the screen into two frames
            self.left_frame = tk.Frame(self, width=self.winfo_screenwidth()//2 )
            self.left_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
            self.right_frame = tk.Frame(self, width=self.winfo_screenwidth() // 2, bg="white")
            self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

            
            # Camera feed on the left frame
            self.canvas = tk.Canvas(self.left_frame, bg='black')
            self.canvas.pack(expand=True, fill=tk.BOTH)

            # Configure the style for tthe widgets
            self.style = ttk.Style(self)
            self.style.configure("TButton", font=("Comic Sans MS", 12), background="black", foreground="Red")
            self.style.configure("TLabel", font=("Comic Sans MS", 12), background="white", foreground=self.text_color)
            self.style.configure("Header.TLabel", font=("Comic Sans MS", 14, "bold"), background="white", foreground=self.titles_color)

            # Close button 
            self.close_btn = ttk.Button(self.right_frame, text="✖", command=self.close_app, style="TButton")
            self.close_btn.pack(side=tk.TOP,  anchor='ne', padx=0, pady=0)


            # Robot, Mode and Speed sections    
            self.robot_label = ttk.Label(self.right_frame, text=f"Robot: {robot_state['Robot']}", style="Header.TLabel")
            self.robot_label.pack(side=tk.TOP,  anchor='nw')
            self.mode_label = ttk.Label(self.right_frame, text=f"Mode: {robot_state['Mode']}", style="Header.TLabel")
            self.mode_label.pack(side=tk.TOP,  anchor='nw')
            self.speed_label = ttk.Label(self.right_frame, text=f"Speed: {robot_state['Speed']}", style="Header.TLabel")
            self.speed_label.pack(side=tk.TOP,  anchor='nw')

            

            # Load command images and initialize them properly
            self.modo_imagem = {key: ImageTk.PhotoImage(Image.open(path)) for key, path in modo_imagem.items()}

            # Image label
            self.image_label = tk.Label(self.right_frame, bg="white", borderwidth=0, highlightthickness=0)
            self.image_label.pack(expand=True, fill=tk.BOTH)
            #self.image_label.place(relx=0.5, rely=0.5, anchor='center', relwidth=0.5, relheight=1)

            self.update_command_image('Camera', 'J')

            # Update the camera feed
            self.update_camera()


    #Thread to update the interface of the robot --> will listen to the terminal
    def change_robot_state(self):
       
       while True:  # Keep listening for messages from the server
            
            try:

                recv_message = s.waitForUpdate(self.client_socket)
                print(recv_message)
                # Split the message into parts
                parts = recv_message.split(', ')

                # Extract and store the robot number
                robot_part = parts[0]
                robot_number = robot_part.split(': ')[1]
            
                # Extract and store the mode
                mode_part = parts[1]
                mode = mode_part.split(': ')[1]

                # Extract and store the speed
                speed_part = parts[2]
                speed = speed_part.split(': ')[1]
                
                menu_part = parts[3]    
                menu = menu_part.split(': ')[1]

                if menu == "True":
                    self.toggle_interface()
                
                # Update the interface with new data
                self.update_interface(robot_number, mode, speed)

            except Exception as e:
                print(f"Error in listen_to_server: {e}")
                break


    #Method to update the interface 
    def update_interface(self, robot, mode, speed):


        if mode == "X":
            mode_changed = 'XYZ'
        elif mode == 'J':
            mode_changed = 'Joint'

        if robot == 'C':
            robot = 'Camera'
        elif robot == 'B':
            robot = 'Bistouri'

        # Use 'after' to schedule the GUI update in the main thread
        self.after(0, lambda: self.robot_label.config(text=f"Robot: {robot}"))
        self.after(0, lambda: self.mode_label.config(text=f"Mode: {mode_changed}"))
        self.after(0, lambda: self.speed_label.config(text=f"Speed: {speed}"))
        self.after(0, lambda: self.update_command_image(robot, mode))
        

    def update_command_image(self, robot, mode):


        robot_str=str(robot)


        # Calculate the intended dimensions
        target_width = self.right_frame.winfo_width()
        target_height = self.right_frame.winfo_height()

        if target_width <= 1 or target_height <= 1:
            target_width = 640
            target_height = 480

        # Get the image key based on the robot and mode
        image_key = (robot_str, mode)
        image_path = modo_imagem.get(image_key)

        
            
        if image_path:
            # Open the image using Pillow
            img = Image.open(image_path)
            # Resize the image proportionally to fit the right frame
            img_aspect_ratio = img.width / img.height
            frame_aspect_ratio = target_width / target_height

            if img_aspect_ratio > frame_aspect_ratio:
                # Image is wider than the frame
                new_width = target_width
                new_height = int(new_width / img_aspect_ratio)
            else:
                # Image is taller than the frame
                new_height = target_height
                new_width = int(new_height * img_aspect_ratio)

            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Convert the image to a Tkinter compatible format
            command_image = ImageTk.PhotoImage(img)

            # Set the image to the label
            self.image_label.config(image=command_image)
            self.image_label.image = command_image  # Keep a reference
            # Position the image label at the center of the right frame
            self.image_label.place(relx=0.5, rely=0.5, anchor='center')
            #self.image_label.pack(expand=True, fill=tk.Y)
            
    
                                   
   #Method to update the camera feed 10fps
    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            
            # Maintain aspect ratio
            frame = cv2.resize(frame, (self.left_frame.winfo_width(), self.left_frame.winfo_height()))
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image
            self.after(20, self.update_camera)
            
                  
    def toggle_interface(self, event=None):
       
        self.full_screen_camera = not self.full_screen_camera

        if self.full_screen_camera:
            # Hide right frame and expand camera
            self.right_frame.pack_forget()
            self.left_frame.config(width=self.winfo_screenwidth())

            
            #self.close_btn.place_configure(self.left_frame)
            #self.close_btn.pack(side=tk.TOP,  anchor='ne', padx=0, pady=0)
            
            
        else:
            # Show right frame and adjust camera
            self.right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)
            self.left_frame.config(width=self.winfo_screenwidth()//2)
            
    

    #Method to close the app
    def close_app(self):
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = CameraApp("Camera Interface")

    # In a real scenario, you would have a loop or a callback that updates the robot_state
    # For example:
    # while True:
    #     current_state = get_robot_state_from_server()
    
        #time.sleep(1)  # Adjust the sleep time as needed    
      
    app.mainloop()
