# Import built-in libraries
import sys
import glob
from collections import namedtuple

# Import local libraries
from lib import create_command, show_info

# Import 3rd party libraries
import tkinter as tk
from tkinter import messagebox
import serial

# Confirm OS compatibility and path delimiter for specfic OS
OS = sys.platform
PATH_DELIMITER = ""

if OS.startswith('win') or OS.startswith('cygwin'):
    PATH_DELIMITER = "\\"
elif OS.startswith('linux') or OS.startswith('darwin'):
    PATH_DELIMITER = "/"
else:
    messagebox.showerror("System not supported", "Your system, %s, is not supported." % OS)
    exit(-1)

# Set Global Variables
WINDOW_SIZE = [400, 300]
TITLE = 'Motor Control Panel'
NO_PORTS_MESSAGE =  'No Ports Detected'
ENTER_COMMAND_MESSAGE = 'Enter a custom command here'
INFO_PRESET_MESSAGE = 'Info will be printed here'
AVAILABLE_BAUDS = ["9600", "19200", "38400"]
COMMANDS = []

# Custom structures for Command and Command Type
CommandType = namedtuple("CommandType", ["name", "path", "commands"])
Command = namedtuple("Command", ["name", "command", "variables", "possible", "values", "description"])

# Main app class with all major app functions
class MotorControlApp(tk.Frame):
    # Constructor initialization function
    def __init__(self, master):
        print("\nInitializing Tkinter frame...\n")
        # Initialize the TK frame
        tk.Frame.__init__(self, master)

        # Load commands into the program
        self.loadCommands()
        
        # Call setup window method passing in splatted window specs
        self.setupWindow(WINDOW_SIZE[0], WINDOW_SIZE[1], *self.calculateWindowOffset())

        # Call setup menu bar method
        self.setupMenuBar()

        print("\nProgram loaded successfully.\n")

    # Load the commands from files into the global COMMANDS array
    def loadCommands(self):
        print("Loading commands...")

        # Clear current commands
        self.clearCommands()

        # Open _types.csv file and iterate through all lines
        count = 0
        for line in open("commands%s_types.csv" % PATH_DELIMITER, 'r').readlines():
            # Split into tokens
            tokens = line.split(',')

            # Append current command type to COMMANDS array
            COMMANDS.append(CommandType(name=tokens[0], path=tokens[1].replace('->', PATH_DELIMITER).replace('\n', ''), commands=[]))

            # Open current command type's commands path and iterate through all lines
            file = open(COMMANDS[count].path, 'r')
            for line in file.readlines():
                # Split into 5 tokens separated by the first 5 commas
                split = line.split(',', 5)

                # If the first token starts with a parenthesis or bracket, re-split lines by first the 7 commas and
                # combine the 1st and 2nd tokens and the 3rd and 4th tokens into one each, then shift the array of tokens accordingly
                if split[0].startswith('[') or split[0].startswith('('):
                    split = line.split(',', 7)
                    split[0] = "%s, %s" % (split[0], split[1])
                    split[1] = "%s, %s" % (split[2], split[3])
                    split[2] = split[4]
                    split[3] = split[5]
                    split[4] = split[6]
                    split[5] = split[7]

                # Append current command to the command type's commands array
                COMMANDS[count].commands.append(Command(split[0], split[1], split[2], split[3], split[4], split[5]))

            # Close the file
            file.close()

            print("\t%s commands were loaded successfully." % COMMANDS[count].name)

            # Increment the line counter
            count += 1

    # Clear the global commands array
    def clearCommands(self):
        COMMANDS = []
        print("\tCommands cleared successfully.")

    # Calculate window position on screen
    def calculateWindowOffset(self):
        # Calculate the x position of the top right corner of the window that is necessary to center it horizontally
        x = (self.master.winfo_screenwidth() / 2) - (WINDOW_SIZE[0] / 2)

        # Calculate the y position of the top right corner of the window that is necessary to center it vertically
        y = (self.master.winfo_screenheight() / 2) - (WINDOW_SIZE[1] / 2)

        return x, y

    # Set up the tkinter window
    def setupWindow(self, width, height, xoffset, yoffset):
        print("Settings up window w=%s, h=%s, xoffset=%s, yoffset=%s..."% (width, height, xoffset, yoffset))

        # Set window to not be resizable and set the title
        self.master.geometry("%dx%d%+d%+d" % (width, height, xoffset, yoffset))
        self.master.resizable(width='false', height='false')
        self.master.title(TITLE)

        # Create master frame
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=width, height=height)
        print("\tframe created successfully.")

        # Create the Command entry box
        self.currentCommand = tk.StringVar()
        self.commandEntry = tk.Entry(self.frame, textvariable=self.currentCommand)
        self.currentCommand.set(ENTER_COMMAND_MESSAGE)
        self.commandEntry.place(x=0, y=0, width=WINDOW_SIZE[0])
        print("\tcommandEntry created successfully.")

        # Create send button
        self.sendButton = tk.Button(self.frame, text='Send Custom Command', command=self.sendCommand)
        self.sendButton.place(x=0, y=18, width=WINDOW_SIZE[0])
        print("\tsendButton created successfully.")

        # Create Option Menu for command types
        self.selectedCommandType = tk.StringVar()
        self.commandTypeMenu = tk.OptionMenu(self.frame, self.selectedCommandType, ())
        self.commandTypeMenu['menu'].config(postcommand=lambda: self.populateCommandTypeMenu())
        self.populateCommandTypeMenu()
        self.commandTypeMenu.place(x=5, y=50, width=147)
        print("\tcommandTypeMenu created successfully.")

        # Create Option Menu for commands
        self.selectedCommand = tk.StringVar()
        self.commandMenu = tk.OptionMenu(self.frame, self.selectedCommand, ())
        self.selectedCommand.set(self.commandMenu["menu"].entrycget(0, "label"))
        self.populateCommandMenu()
        self.commandMenu.place(x=157, y=50, width=93)
        print("\tcommandMenu created successfully.")

        # Create Button to send command
        self.sendCommandButton = tk.Button(self.frame, text='Send Command', command=lambda: self.sendCommand(self.getCommand()))
        self.sendCommandButton.place(x=255, y=52, width=WINDOW_SIZE[0]-260, height=27)
        print("\tsendCommandButton created successfully.")

        # Create Button to edit the current command
        self.editCommandButton = tk.Button(self.frame, text='Edit Command', command=lambda: self.editCommand(self.getCommand()))
        self.editCommandButton.place(x=255, y=84, width=WINDOW_SIZE[0]-260, height=27)
        print("\teditCommandButton created successfully")

        # Create Button to delete the current command
        self.deleteCommandButton = tk.Button(self.frame, text='Delete Command', command=lambda: self.deleteCommand(self.getCommand()))
        self.deleteCommandButton.place(x=255, y=116, width=WINDOW_SIZE[0]-260, height=27)
        print("\tdeleteCommandButton created successfully")

        # Create Info entry box
        self.info = tk.StringVar()
        self.infoLabel = tk.Entry(self.frame, textvariable=self.info, state='readonly', width=WINDOW_SIZE[0])
        self.info.set(INFO_PRESET_MESSAGE)
        self.infoLabel.place(x=0, y=WINDOW_SIZE[1]-18)
        print("\tinfoLabel created successfully.")

        # Set method for when user clicks the window's 'x' button
        self.master.protocol("WM_DELETE_WINDOW", self.quitApp)
        print("\tX-button action set to quitApp successfully")

    # Send a command through the selected serial port
    def sendCommand(self, command=None):
        # If there is a valid port seleted send the command, else display select a port message
        if self.selectedPort.get() and self.selectedPort.get() != NO_PORTS_MESSAGE:
            # Get selected port and baud
            port = self.selectedPort.get()
            baud = int(self.selectedBaud.get())

            # Open the serial port and set baud rate
            ser = serial.Serial(port)
            ser.baudrate = baud

            # If port opened successfully, send the command, else display message
            if ser.isOpen():
                # If no command was passed in, send command currently entered in command entry, else send selected command
                if command == None:
                    ser.write(self.currentCommand.get().encode())
                    self.info.set('Sending "%s" to %s at %s BAUD...' % (self.currentCommand.get(), port, baud))
                else:
                    ser.write(command.command.encode())
                    self.info.set('Sending "%s" to %s at %s BAUD...' % (command.name, port, baud))

                # Close the serial port
                ser.close()
            else:
                self.info.set("%s failed to open properly." % ser.name)
        else:
            self.info.set("Please select a port first.")

    # Populate the Command Type menu
    def populateCommandTypeMenu(self):
        print("\tPopulating commandTypeMenu...")

        # Delete current menu entries
        self.commandTypeMenu['menu'].delete(0, 'end')

        # For each command type, add an entry to the menu
        for type in COMMANDS:
            self.commandTypeMenu['menu'].add_command(label=type.name, command=lambda value=type.name:self.setTypeAndPopulateCommandsMenu(value))
            print("\t\t%s command type loaded successfully." % type.name)

        # If there is not a selected command type, set selected command type to first in the menu
        if not self.selectedCommandType.get():
            self.selectedCommandType.set("Operation Stored")

    # Set selected command type and populate the command menu accordingly
    def setTypeAndPopulateCommandsMenu(self, ctype):
        self.selectedCommandType.set(ctype)
        self.populateCommandMenu()

    # Populate the commands menu to display commands of selected type
    def populateCommandMenu(self):
        print("\tPopulating commandMenu with %s commands..." % self.selectedCommandType.get())

        # Delete current menu entries
        self.commandMenu["menu"].delete(0, "end")

        # For each command, add an entry to the menu
        for command in self.getCommandsOfType(self.selectedCommandType.get(), 'true'):
            self.commandMenu["menu"].add_command(label=command, command=lambda value=command: self.selectedCommand.set(value))
            print("\t\t%s command loaded successfully." % command)

        # Set selected command to first in the menu
        self.selectedCommand.set(self.commandMenu["menu"].entrycget(0, "label"))

    # Get the currently selected command
    def getCommand(self):
        commands = self.getCommandsOfType(self.selectedCommandType.get())

        # For each command, check if name is equal to currently selected command option
        for command in commands:
            if command.name == self.selectedCommand.get():
                return command

    # Get list of commands of specified type
    def getCommandsOfType(self, ctype, namesOnly='false'):
        # Create return object
        ret = []

        # Append each command to return object
        for command in self.getCommandType(ctype).commands:
            # If namesOnly is true, append only the name of the command else append the whole command object.
            if (namesOnly == 'true'):
                ret.append(command.name)
            else:
                ret.append(command)

        # Return list
        return ret

    # Get the command type object with the specified name
    def getCommandType(self, ctype):
        # For each command type in COMMANDS check if name is equal to specified name
        count = 0
        for commandType in COMMANDS:
            # If name = specified name, return the command type object
            if commandType.name == ctype:
                return COMMANDS[count]

            # Increment counter
            count += 1

        print("getCommandType(%s) returned nothing." % ctype)

    # Edit the selected command
    def editCommand(self, command):
        # TODO
        print("\tEdit button clicked for command ->", command)

    # Delete the specified command
    def deleteCommand(self, command):
        # TODO
        print("\tDelete button clicked for command ->", command)

    # Quit the application
    def quitApp(self):
        # Show messagebox asking is the user is sure they want to quit
        if messagebox.askyesno("Quit?", "Are you sure you want to quit?"):
            # If settings window is opened, kill it
            if hasattr(self, 'settingsWindow') and self.settingsWindow.status == 'running':
                self.settingsWindow.quit()

            # If create command window is opened, kill it
            if hasattr(self, 'createCommandWindow') and self.createCommandWindow.status == 'running':
                self.createCommandWindow.quit()

            # If info window is opened, kill it
            if hasattr(self, 'createInfoWindow') and self.createInfoWindow.status == 'running':
                self.createInfoWindow.quit()

            # Destroy application
            self.master.destroy()

    # Set up the menu bar for the application
    def setupMenuBar(self):
        print("Setting up menu bar...")

        # Create a menu bar
        self.menuBar = tk.Menu(self.master)

        # Create the file menu
        self.createFileMenu()

        # Create the edit menu
        self.createEditMenu()

        # Create the serial menu
        self.createSerialMenu()

        # Create the help menu
        self.createHelpMenu()

        # Add the menu bar to the master window
        self.master.config(menu=self.menuBar)

        print("\tMenu bar configuration completed successfully.")

    # Create the file menu for menu bar
    def createFileMenu(self):
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="New Command...", command= self.createCommand)
        self.fileMenu.add_command(label="Load Commands...", command=self.loadCommandType)
        self.fileMenu.add_command(label="Load Program...", command=self.loadProgram)
        self.fileMenu.add_command(label="Save Command As...", command=self.saveCommandAs)
        self.fileMenu.add_command(label="Save Command Type As...", command=self.saveCommandTypeAs)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.quitApp)

        # Add file menu to menu bar
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        print("\tFile menu created successfully.")

    # Show the create command window
    def createCommand(self):
        self.createCommandWindow = create_command.CreateCommandApp(tk.Tk(), COMMANDS)
        self.createCommandWindow.run()

    # Show the open command type dialog
    def loadCommandType(self):
        # TODO
        print("\tloadCommandType() called.")

    # Load a program from a file
    def loadProgram(self):
        # TODO
        print("\tloadProgram() called.")

    # Save the current command
    def saveCommandAs(self):
        # TODO
        print("\tsaveCommandAs() called.")

    # Show the save command type as dialog
    def saveCommandTypeAs(self):
        # TODO
        print("\tsaveCommandTypeAs() called.")

    # Create the edit menu for menu bar
    def createEditMenu(self):
        self.editMenu = tk.Menu(self.frame, tearoff=0)
        self.editMenu.add_command(label="Edit Command...", command=lambda: self.editCommand(self.getCommand()))
        self.editMenu.add_command(label="Delete Command", command=lambda: self.deleteCommand(self.getCommand()))
        self.editMenu.add_command(label="Rename Command  Type...", command=self.renameCommandType)
        self.editMenu.add_command(label="Delete Command Type", command=self.deleteCommandType)

        # Add edit menu to menu bar
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)

    # Rename the current command type
    def renameCommandType(self):
        # TODO
        print("\trenameCommandType() called.")

    # Delete all commands in the current type and the type itself
    def deleteCommandType(self):
        # TODO
        print("\tdeleteCommandType() called.")

    # Create the serial menu
    def createSerialMenu(self):
        # Create the port and baud menus and variables
        self.selectedPort = tk.StringVar()
        self.selectedBaud = tk.StringVar()
        self.serialMenu = tk.Menu(self.menuBar, tearoff=0)
        self.portMenu = tk.Menu(self.serialMenu, tearoff=0, postcommand=lambda: self.populatePortMenu())
        self.baudMenu = tk.Menu(self.serialMenu, tearoff=0, postcommand=lambda: self.populateBAUDMenu())

        # Populate the ports menu
        self.populatePortMenu()

        # Populate the BAUD menu
        self.populateBAUDMenu()

        # Add port and baud menus to serial menu
        self.serialMenu.add_cascade(label="Port", menu=self.portMenu)
        self.serialMenu.add_cascade(label="BAUD", menu=self.baudMenu)

        # Add serial menu to menubar
        self.menuBar.add_cascade(label="Serial", menu=self.serialMenu)

        print("\tSerial menu created successfully.")

    # Populate the ports menu
    def populatePortMenu(self):
        print("\tPopulating port menu...")

        # Delete current menu entries
        self.portMenu.delete(0, 'end')

        # Get current available ports
        self.availablePorts = self.getAvailablePorts()

        # If no available ports are in the lsit, populate available ports with no ports message
        if not self.availablePorts:
            self.availablePorts = [NO_PORTS_MESSAGE]

        # For each available port, add a menu radiobutton
        for port in self.availablePorts:
            self.portMenu.add_radiobutton(label=port, variable=self.selectedPort, value=port)

        print("\t\tAvailable ports scanned successfully. -> %s" % ", ".join(self.availablePorts))

    # Get all currently available com ports
    def getAvailablePorts(self):
        # Check system platform and populate possible ports accordingly
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # This is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        # Scan ports and add available ones to result list
        result = []
        for port in ports:
            # Attempt to open the port. If unsuccessfuly, pass exception
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        # Return list of available ports
        return result

    # Populate the BAUD menu
    def populateBAUDMenu(self):
        print("\tPopulating BAUD menu...")

        # Delete current menu entries
        self.baudMenu.delete(0, 'end')

        # If no available BAUD is selected, set selected Baud to first in the list.
        if not self.selectedBaud.get():
            self.selectedBaud.set(AVAILABLE_BAUDS[0])

        # For each available BAUD, add a menu radiobutton
        for baud in AVAILABLE_BAUDS:
            self.baudMenu.add_radiobutton(label=baud, variable=self.selectedBaud, value=baud)

        print("\t\tAvailable BAUDs loaded successfully. -> %s" % ", ".join(AVAILABLE_BAUDS))

    # Create the help menu and add to menu bar
    def createHelpMenu(self):
        # Create help, command, immediate, and programStored menus
        self.helpMenu = tk.Menu(self.menuBar, tearoff=0)
        self.commandsMenu = tk.Menu(self.helpMenu, tearoff=0, postcommand=lambda: self.populateCommandsHelpMenu())
        self.immediateMenu = tk.Menu(self.commandsMenu, tearoff=0)
        self.programStoredMenu = tk.Menu(self.commandsMenu, tearoff=0)

        # Add immediate and programStored menus to commands menu
        self.commandsMenu.add_cascade(label="Immediate", menu=self.immediateMenu)
        self.commandsMenu.add_cascade(label="Program Stored", menu=self.programStoredMenu)

        # Populate the commands menu
        self.populateCommandsHelpMenu()

        # Add commands menu to help menu
        self.helpMenu.add_cascade(label="Commands", menu=self.commandsMenu)

        # Add a separator
        self.helpMenu.add_separator()

        # Add about entry to help menu
        self.helpMenu.add_command(label="About", command=lambda: self.showAbout())

        # Add help menu to menu bar
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)

        print("\tHelp menu created successfully.")

    # Populate the commands help menu
    def populateCommandsHelpMenu(self):
        print("\tPopulating commandsMenu...")

        # Set counter and delete commands from commands menu
        self.commandsMenu.delete(2, 'end')
        self.immediateMenu.delete(0, 'end')
        self.programStoredMenu.delete(0, 'end')

        # For each command type object in COMMANDS, check the name and place it in the appropriate menu
        for ctype in COMMANDS:
            # For first two types, place is immediate menu
            if ctype.name == "Operation Stored" or ctype.name == "Status Request":
                tempMenu = self.immediateMenu
            # For next four types, place in program stored menu
            elif ctype.name == "Motor" or ctype.name == "Looping/Branching" or ctype.name == "Pausing" or ctype.name == "Input/Output":
                tempMenu = self.programStoredMenu
            # For all other types, place directly in commands menu, adding a separator before first other command type
            else:
                tempMenu = self.commandsMenu
                if ctype.name == "Custom":
                    tempMenu.add_separator()

            # Add the current command type to the selected menu
            tempMenu.add_command(label=ctype.name, command=lambda value=ctype.name:self.showCommands(value))

            print("\t\t%s help option loaded successfully." % ctype.name)

    # Display the commands dialog window
    def showCommands(self, ctype):
        self.createInfoWindow = show_info.ShowInfoApp(tk.Tk(), ctype, self.getCommandsOfType(ctype))
        self.createInfoWindow.run()

    # Display messagebox with information about this application
    def showAbout(self):
        messagebox.showinfo("About This Motor Controller", "This controller was written by Ian Tait for the Physics Department of the University of Kansas for the purpose of programming the VXM motor controller. This project is for a capstone class proctored by Dr. Graham Wilson.")

    # Run the application
    def run(self):
        self.mainloop()
