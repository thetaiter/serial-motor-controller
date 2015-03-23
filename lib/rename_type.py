import tkinter as tk

WINDOW_SIZE = [300, 60]
TITLE = "Rename: "

# Show info application main class
class RenameTypeApp(tk.Frame):
    # Constructor initialization class
    def __init__(self, master, ctype, callback):
        # Initialize the TK frame
        tk.Frame.__init__(self, master)

        self.ctype = ctype
        self.callback = callback

        # Set window geometry, position and title
        self.xPos, self.yPos = self.calculateWindowOffset()
        self.master.geometry("%dx%d%+d%+d" % (WINDOW_SIZE[0], WINDOW_SIZE[1], self.xPos, self.yPos))
        self.master.resizable(width='false', height='false')
        self.master.title(TITLE + self.ctype.name)

        # Create frame for object in window
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

        # Create and place label
        self.label = tk.Label(self.frame, text="New Type Name:")
        self.label.place(x=5, y=5, width=90)

        # Create and place entry
        self.entry = tk.Entry(self.frame)
        self.entry.place(x=100, y=5, width=WINDOW_SIZE[0]-105)

        self.okButton = tk.Button(self.frame, text='OK', command=self.okClicked)
        self.okButton.place(x=5, y=30, width=(WINDOW_SIZE[0]-10)/2)

        self.cancelButton = tk.Button(self.frame, text='Cancel', command=self.quit)
        self.cancelButton.place(x=(WINDOW_SIZE[0]/2)+5, y=30, width=((WINDOW_SIZE[0]-10)/2)-5)

        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    # Calculate window position on screen
    def calculateWindowOffset(self):
        # Calculate the x position of the top right corner of the window that is necessary to center it horizontally
        x = (self.master.winfo_screenwidth() / 2) - (WINDOW_SIZE[0] / 2)

        # Calculate the y position of the top right corner of the window that is necessary to center it vertically
        y = (self.master.winfo_screenheight() / 2) - (WINDOW_SIZE[1] / 2)

        return x, y

    def okClicked(self):
        self.callback(self.entry.get())

        self.quit()

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