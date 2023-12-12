import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class CameraApp(tk.Tk):

    # Initializing the camera
    def __init__(self, window_title="Interface"):
        super().__init__()

        self.title(window_title)    
        # Open the camera (you may need to adjust the camera index)
        self.cap = cv2.VideoCapture(0)

        # Display robot mode with a bold and larger font
        self.robot_mode_label = tk.Label(self, text="Mode: XYZ", font=("Helvetica", 14, "bold"))
        self.robot_mode_label.pack(pady=10)

        # Display robot selector with a bold font and different color
        self.robot_selector_label = tk.Label(self, text="Robot: Robot 1", font=("Helvetica", 12, "bold"), fg="blue")
        self.robot_selector_label.pack(pady=5)

        # Create a button to close the app with a themed style
        self.close_btn = ttk.Button(self, text="Close", command=self.close_app, style="TButton")
        self.close_btn.pack(pady=20)

        # Create a frame to hold the camera feed
        self.camera_frame = tk.Frame(self)
        self.camera_frame.pack(expand=tk.YES, fill=tk.BOTH)

        # Create a canvas to display the camera feed
        self.canvas = tk.Canvas(self.camera_frame, width=1600, height=900)
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Update the camera display (replace this with your camera feed)
        self.update()

        # Configure styles for themed widgets
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 12))

    def update(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        if ret:
            # Get the dimensions of the window
            width, height = self.winfo_screenwidth(), self.winfo_screenheight()
            
            # Resize the frame to full screen
            frame = cv2.resize(frame, (width, height))

            # Convert the OpenCV frame to a PIL image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)

            # Update the canvas with the new image
            self.canvas.config(width=width, height=height)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=image)
            self.canvas.image = image  # Keep a reference to prevent garbage collection

            # Call the update method again after a delay (e.g., 33 milliseconds for 30 fps)
            self.after(10, self.update)


    def close_app(self):
        # Release the camera and close the app
        self.cap.release()
        self.destroy()

# Create the main window
if __name__ == "__main__":

    app = CameraApp("Camera App")

     # Make the window fullscreen
    app.attributes("-fullscreen", True)

    # Start the Tkinter event loop
    app.mainloop()
