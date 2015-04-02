# Import local libraries
from lib import command
Command = command.Command

# Import 3rd party libraries
import tkinter as tk

# Set global variables
WINDOW_SIZE = [525, 600]
MAX_CHARS_IN_LINE = 50
TITLE = "Show Info"

# Show info application main class
class ShowInfoApp(tk.Frame):
    # Constructor initialization class
    def __init__(self, master, type, commands):
        # Initialize the TK frame
        tk.Frame.__init__(self, master)

        # Setup the show info window
        self.setupWindow(type, commands)

        # Set app status to initialized
        self.status = 'initiated'

    # Setup the tkinter window and frame
    def setupWindow(self, type, commands):
        # Set title to command type
        TITLE = "%s Commands Information" % type

        # Set window geometry, position and title
        self.xPos, self.yPos = self.calculateWindowOffset()
        self.master.geometry("%dx%d%+d%+d" % (WINDOW_SIZE[0], WINDOW_SIZE[1], self.xPos, self.yPos))
        self.master.resizable(width='false', height='false')
        self.master.title(TITLE)

        # Create frame for object in window
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

        # Create scrollbar to scroll through commands
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.place(x=WINDOW_SIZE[0]-17, y=0, height=WINDOW_SIZE[1]-30)

        # Create and place command info textbox and set scrollbar and word wrap
        self.infoTextBox = tk.Text(self.frame, width=WINDOW_SIZE[0]-17, height=WINDOW_SIZE[1]-30, yscrollcommand=self.scrollbar.set, wrap=tk.WORD)
        self.infoTextBox.place(x=0, y=0, width=WINDOW_SIZE[0]-17, height=WINDOW_SIZE[1]-30)

        # Set margin for all lines that have been wrapped
        self.infoTextBox.tag_configure('n', lmargin2=104)

        # Lock the scrollbar to the y position of the textbox
        self.scrollbar.config(command=self.infoTextBox.yview)

        # Create and place the OK button
        self.okButton = tk.Button(self.frame, text="OK", command=self.quit)
        self.okButton.place(x=(WINDOW_SIZE[0] - 100)/2, y=WINDOW_SIZE[1]-27, width=100)

        # For each command in the list of commands, format it and append it in the textbox
        for command in self.formatCommands(commands):
            self.infoTextBox.insert('end', command, 'n')

        # Set textbox state to disabled
        self.infoTextBox.config(state=tk.DISABLED)

        # Set method for when user clicks the window's 'x' button
        self.master.protocol("WM_DELETE_WINDOW", self.quit)

    # Calculate window position on screen
    def calculateWindowOffset(self):
        # Calculate the x position of the top right corner of the window that is necessary to center it horizontally
        x = (self.master.winfo_screenwidth() / 2) - (WINDOW_SIZE[0] / 2)

        # Calculate the y position of the top right corner of the window that is necessary to center it vertically
        y = (self.master.winfo_screenheight() / 2) - (WINDOW_SIZE[1] / 2)

        return x, y

    # Format commands to clean output
    def formatCommands(self, commands):
        # Initialize return object
        ret = []

        # For each command, append the formatted information to return object
        for command in commands:
            variables = []
            possibles = []
            currents = []

            if command.getVariables():
                for v in command.getVariables():
                    variables.append(v.getSymbol())
                    possibles.append(str(v.getLow()) + " - " + str(v.getHigh()))
                    currents.append(str(v.getCurrentValue()))

            ret.append("Name: %s\nCommand: %s\nVariables: %s\nPossible Values: %s\nCurrent Values: %s\nDescription: %s\n\n" % (command.getName(), command.getCommandRaw(), ', '.join(variables), ', '.join(possibles), ', '.join(currents), command.getDescription()))

        # Return formatted commands
        return ret

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
