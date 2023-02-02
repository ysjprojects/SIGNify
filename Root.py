import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time

import customtkinter

customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

class Root:

    def __init__(self):
        self.window = customtkinter.CTk()

        # Create the GUI window
        self.window.geometry("1280x720")
        # Create a label to display the webcam feed
        self.webcam_label = customtkinter.CTkLabel(self.window, text="")
        self.webcam_label.pack(padx=25,pady=25,side="top", anchor="nw")

        # Initialize the webcam
        self.webcam = cv2.VideoCapture(0)
        if not self.webcam.isOpened():
            raise Exception("Could not open video device")
        # Set properties. Each returns === True on success (i.e. correct resolution)
        self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        self.last_updated_at = 0
        # Initialize the time of the last saved frame

        self.capture_on_right = True #Default: right side of the screen
        
        self.is_captured = False

        # Start updating the GUI
        self.update_frame()

    def get_capture_zone_border_color(self):
        # BGR format
        return (60,20,220) if not self.is_captured else (51,163,90)


    @staticmethod
    def get_capture_zone_position(parent_height, is_right):
        # returns x1, y1, x2,y2
        if is_right:
            return int(0.5 * parent_height), 10, parent_height - 10, int(0.5 * parent_height)
        
        else:
            return 10, 10, int(0.5 * parent_height), int(0.5 * parent_height)

    def update_frame(self):
        _, frame = self.webcam.read()
        frame = cv2.flip(frame, 1)
        
        x1, y1, x2, y2 = self.get_capture_zone_position(frame.shape[1], self.capture_on_right)
        print(f"{x1},{y1},{x2},{y2}")
        cv2.rectangle(frame, (x1-1,y1-1), (x2+1,y2+1), self.get_capture_zone_border_color() ,2)
        
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        img = PIL.Image.fromarray(cv2image)
        imgtk = PIL.ImageTk.PhotoImage(image=img)
        self.webcam_label.imgtk = imgtk
        self.webcam_label.configure(image=imgtk)

        cap_img = cv2image[y1:y2,x1:x2]



        # Save the frame every 500 milliseconds
        current_time = time.time()
        if current_time - self.last_updated_at >= 1:
            cv2.imwrite("captured_frame.jpg", cap_img)
            self.last_updated_at = current_time
            
        self.window.after(10, self.update_frame)






# Run the GUI loop
(Root()).window.mainloop()