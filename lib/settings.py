# Import 3rd party libraries
import tkinter as tk
from tkinter import messagebox

# Create global variables
WINDOW_SIZE = [300, 200]
TITLE = "Settings"

# Class for the settings app
class SettingsApp(tk.Frame):
    # Constructor Initialization function
    def __init__(self, master):
        # Initialize the TK frame
        tk.Frame.__init__(self, master)

        # Setup window geometry, position and title
        self.xPos, self.yPos = self.calculateWindowOffset()
        self.master.geometry("%dx%d%+d%+d" % (WINDOW_SIZE[0], WINDOW_SIZE[1], self.xPos, self.yPos))
        self.master.resizable(width='false', height='false')
        self.master.title(TITLE)

        # Create frame for objects in window
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

        # Create and place numMotorsLabel
        self.numMotorsLabel = tk.Label(self.frame, text="# of Motors:")
        self.numMotorsLabel.place(x=10, y=15, width=65)

        # Creat numMotors variable and menu and place on frame
        self.numMotors = tk.IntVar()
        self.numMotorsMenu = tk.OptionMenu(self.frame, self.numMotors, 1, 2, 3, 4)
        self.numMotors.set(1)
        self.numMotorsMenu.place(x=80, y=10, width=50)

        # Set method for when user clicks the window's 'x' button
        self.master.protocol("WM_DELETE_WINDOW", self.quitApp)

        # Set app status to initiated
        self.status = 'initiated'
        
    # Calculate window position on screen
    def calculateWindowOffset(self):
        # Calculate the x position of the top right corner of the window that is necessary to center it horizontally
        x = (self.master.winfo_screenwidth() / 2) - (WINDOW_SIZE[0] / 2)

        # Calculate the y position of the top right corner of the window that is necessary to center it vertically
        y = (self.master.winfo_screenheight() / 2) - (WINDOW_SIZE[1] / 2)

        return x, y

    # Save the current settings
    def saveSettings(self):
        print("Settings saved.")

    # Quit the application
    def quitApp(self):
        # If user confirms they want to save settings, settings are saved, else settings are not saved
        if messagebox.askyesno("Save Settings?", "Would you like to save your settings?"):
            self.saveSettings()

        # Close the application
        self.quit()

    # Close the application
    def quit(self):
        # Set app status to destroyed
        self.status = 'destroyed'

        # Destroy the application
        self.master.destroy()

    # Run the application
    def run(self):
        self.status = 'running'
        self.mainloop()
