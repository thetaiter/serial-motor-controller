import tkinter as tk

WINDOW_SIZE = [300, 150]
TITLE = "Rename Type..."

# Show info application main class
class RenameTypeApp(tk.Frame):
    # Constructor initialization class
    def __init__(self, master, ctype):
        # Initialize the TK frame
        tk.Frame.__init__(self, master)

        # Set window geometry, position and title
        self.xPos, self.yPos = self.calculateWindowOffset()
        self.master.geometry("%dx%d%+d%+d" % (WINDOW_SIZE[0], WINDOW_SIZE[1], self.xPos, self.yPos))
        self.master.resizable(width='false', height='false')
        self.master.title(TITLE)

        # Create frame for object in window
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

    # Calculate window position on screen
    def calculateWindowOffset(self):
        # Calculate the x position of the top right corner of the window that is necessary to center it horizontally
        x = (self.master.winfo_screenwidth() / 2) - (WINDOW_SIZE[0] / 2)

        # Calculate the y position of the top right corner of the window that is necessary to center it vertically
        y = (self.master.winfo_screenheight() / 2) - (WINDOW_SIZE[1] / 2)

        return x, y

    # Close the application
    def quit(self):
        # Set app status to  destroyed
        self.status = 'destroyed'

        # Destroy the application
        self.master.destroy()

    # Run the application
    def run(self):
        self.status = 'running'
        self.mainloop()