# Import built-in libraries
import sys
import os
import glob
import shutil

# Import local libraries
from lib import create_command, show_info, rename_type, command_type, command, variable

CreateCommandApp = create_command.CreateCommandApp
ShowInfoApp = show_info.ShowInfoApp
RenameTypeApp = rename_type.RenameTypeApp
Command = command.Command
CommandType = command_type.CommandType
Variable = variable.Variable

# Import 3rd party libraries
import tkinter as tk
from tkinter import messagebox, filedialog
import serial

# Set Global Variables
WINDOW_SIZE = [400, 300]
TITLE = 'Motor Control Panel'
NO_PORTS_MESSAGE =  'No Ports Detected'
ENTER_COMMAND_MESSAGE = 'Enter a custom command here'
INFO_PRESET_MESSAGE = 'Info will be printed here'
AVAILABLE_BAUDS = ["9600", "19200", "38400"]

# Main app class with all major app functions
class MotorControlApp(tk.Frame):
    # Constructor initialization function
    def __init__(self, master):
        print("\nInitializing Tkinter frame...\n")

        # Initialize the TK frame
        tk.Frame.__init__(self, master)

        self.setup = False
        self.program = ''

        # Load commands into the program
        self.loadCommands()
        
        # Call setup window method passing in splatted window specs
        self.setupWindow(WINDOW_SIZE[0], WINDOW_SIZE[1], *self.calculateWindowOffset())

        # Call setup menu bar method
        self.setupMenuBar()

        print("\nProgram loaded successfully.\n")

    # Load the commands from files into the global self.COMMANDS array
    def loadCommands(self):
        print("Loading commands...")

        # Clear current commands
        self.clearCommands()

        # Open _types.csv file and iterate through all lines
        count = 0
        typesFile = open("commands%s_types.csv" % os.sep, 'r')
        lines = typesFile.readlines()
        typesFile.close()

        for line in lines:
            # Split into tokens
            tokens = line.split(',')

            # Append current command type to self.COMMANDS array
            if len(tokens) < 2:
                path = ""
            else:
                path = tokens[1].replace('->', os.sep).replace('\n', '')
            self.COMMANDS.append(CommandType(name=tokens[0], path=path, commands=[]))

            print("\tLoading %s commands..." % self.COMMANDS[count].name)

            # Open current command type's commands path and iterate through all lines
            if os.path.isfile(self.COMMANDS[count].path):
                file = open(self.COMMANDS[count].path, 'r')
                for line in file.readlines():
                    # Split into 5 tokens separated by the first 5 commas
                    split = line.split(',', 5)
                    # If the first token starts with a parenthesis or bracket, re-split lines by first the 7 commas and
                    # combine the 1st and 2nd tokens and the 3rd and 4th tokens into one each, then shift the array of tokens accordingly
                    if split[0].startswith('[') or split[0].startswith('('):
                        split = line.split(',', 7)
                        split[0] = "%s, %s" % (split[0], split[1].replace(' ', '', 1))
                        split[1] = "%s, %s" % (split[2], split[3].replace(' ', '', 1))
                        split[2] = split[4]
                        split[3] = split[5]
                        split[4] = split[6]
                        split[5] = split[7]

                    vars = []
                    if split[2]:
                        c = 0
                        for v in split[2]:
                            low = split[3].split()[c].split('-')[0]

                            if isinstance(low, str) and low == '':
                                low = 0 - int(split[3].split()[c].split('-')[1])
                                high = int(split[3].split()[c].split('-')[2])
                            elif low == 'range':
                                low = -1000000
                                high = 1000000
                            else:
                                low = int(split[3].split()[c].split('-')[0])
                                high = int(split[3].split()[c].split('-')[1])

                            vars.append(Variable(symbol=v, low=low, high=high, currentValue=int(split[4].split()[c])))
                            c += 1

                    # Append current command to the command type's commands array
                    self.COMMANDS[count].getCommands().append(Command(name=split[0], command=split[1], variables=vars, description=split[5].replace('\n', ''), frame=tk.Frame()))

                    print("\t\t%s command loaded successfully." % self.COMMANDS[count].getCommands()[-1].getName())

                # Close the file
                file.close()

                print("\t%s commands were loaded successfully." % self.COMMANDS[count].getName())

                # Increment the line counter
                count += 1
            else:
                name = self.COMMANDS[count].getName()

                del(self.COMMANDS[count])

                file = open("commands%s_types.csv" % os.sep, 'w')
                for l in lines:
                    if not l.__contains__(name):
                        file.write(l)

        if self.setup == True:
            self.selectedCommandType.set(self.commandTypeMenu['menu'].entrycget(0, 'label'))

    # Clear the global commands array
    def clearCommands(self):
        self.COMMANDS = []
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
        self.master.resizable(width=False, height=False)
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
        self.sendCommandButton = tk.Button(self.frame, text='Send Command', command=lambda: self.sendCommand(self.getCurrentCommand()))
        self.sendCommandButton.place(x=255, y=52, width=WINDOW_SIZE[0]-260, height=27)
        print("\tsendCommandButton created successfully.")

        # Create Button to edit the current command
        self.editCommandButton = tk.Button(self.frame, text='Edit Command', command=lambda: self.editCommand(self.getCurrentCommand()))
        self.editCommandButton.place(x=255, y=84, width=WINDOW_SIZE[0]-260, height=27)
        print("\teditCommandButton created successfully")

        # Create Button to delete the current command
        self.deleteCommandButton = tk.Button(self.frame, text='Delete Command', command=lambda: self.deleteCommand(self.getCurrentCommand()))
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

        self.setup = True

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
                    ser.write(command.getCommand().encode())
                    self.info.set('Sending "%s" to %s at %s BAUD...' % (command.getCommand(), port, baud))

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
        for type in self.COMMANDS:
            self.commandTypeMenu['menu'].add_command(label=type.getName(), command=lambda value=type.getName():self.setTypeAndPopulateCommandsMenu(value))
            print("\t\t%s command type loaded successfully." % type.getName())

        # If there is not a selected command type, set selected command type to first in the menu
        if not self.selectedCommandType.get():
            self.selectedCommandType.set(self.commandTypeMenu['menu'].entrycget(0, 'label'))

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
        for command in self.getCommandsOfType(self.selectedCommandType.get(), namesOnly=True):
            self.commandMenu["menu"].add_command(label=command, command=lambda value=command: self.selectedCommand.set(value))
            print("\t\t%s command loaded successfully." % command)

        # Set selected command to first in the menu
        self.selectedCommand.set(self.commandMenu["menu"].entrycget(0, "label"))

    # Get the currently selected command
    def getCurrentCommand(self):
        commands = self.getCommandsOfType(self.selectedCommandType.get())

        # For each command, check if name is equal to currently selected command option
        for command in commands:
            if command.getName() == self.selectedCommand.get():
                return command

    # Get list of commands of specified type
    def getCommandsOfType(self, ctype, namesOnly=False):
        # Create return object
        ret = []

        # Append each command to return object
        for command in self.getCommandType(ctype).getCommands():
            # If namesOnly is true, append only the name of the command else append the whole command object.
            if (namesOnly == True):
                ret.append(command.getName())
            else:
                ret.append(command)

        # Return list
        return ret

    # Get the command type object with the specified name
    def getCommandType(self, ctype):
        # For each command type in self.COMMANDS check if name is equal to specified name
        count = 0
        for commandType in self.COMMANDS:
            # If name = specified name, return the command type object
            if commandType.getName() == ctype:
                return self.COMMANDS[count]

            # Increment counter
            count += 1

        print("\tgetCommandType(%s) returned nothing." % ctype)

    # Edit the selected command
    def editCommand(self, command):
        if command is not None:
            self.createCommandWindow = CreateCommandApp(tk.Tk(), self.COMMANDS, command, self.selectedCommandType.get(), lambda: self.populateCommandMenu())
            self.createCommandWindow.run()
        else:
            self.info.set("Invalid command selected.")

    # Delete the specified command
    def deleteCommand(self, command):
        # Display messagebox to alert user of deletion
        if messagebox.askyesno('Delete Command?', "Are you sure you would like to delete the command '%s'?\nThis will be permanent." % command.getName()):
            # Get indexes of type and command
            typeIndex, comIndex = self.getCommandIndex(command)

            # If command exists, delete it from the list of commands
            if typeIndex != -1 and comIndex != -1:
                del(self.COMMANDS[typeIndex].getCommands()[comIndex])

                # Read file where command originated from
                file = open(self.getPath(self.selectedCommandType.get()), 'r')
                lines = file.readlines()
                file.close()

                # Overwrite the file with all entries except desired command to delete
                with open(self.getPath(self.selectedCommandType.get()), 'w') as file:
                    for line in lines:
                        if not line.startswith(command.name):
                            file.write(line)
                    file.close()

                self.populateCommandMenu()

                print("\tCommand '%s' was deleted successfully." % command.getName())
            else:
                print("\nCommand '%s' was not found." % command.getName())

    # Get the index of the command's type in the global self.COMMANDS array and the index of the command within the commands array of that type
    def getCommandIndex(self, command):
        # For each type in self.COMMANDS, iterate through commands
        typeCount = 0
        for ctype in self.COMMANDS:
            comCount = 0
            for com in ctype.getCommands():
                # If command name is same as desired command, return index of type and command
                if com.getName() == command.getName():
                    return typeCount, comCount
                # Incrememnt command counter
                comCount += 1
            #Incrememnt type counter
            typeCount += 1

        # If command was not found, return negative values
        return -1, -1

    # Get the file path of the commands that are of the specified type
    def getPath(self, ctype):
        for ct in self.COMMANDS:
            if ct.getName() == ctype:
                return ct.getPath()

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

            if hasattr(self, 'renameTypeWindow') and self.renameTypeWindow.status == 'running':
                self.renameTypeWindow.quit()

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
        self.fileMenu.add_command(label="Load Program...", command=self.loadProgram)
        self.fileMenu.add_command(label="Load Command Type...", command=self.loadCommandType)
        self.fileMenu.add_command(label="Save Command Type...", command=lambda:self.saveCommandType(As=False))
        self.fileMenu.add_command(label="Save Command Type As...", command=self.saveCommandType)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.quitApp)

        # Add file menu to menu bar
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

        print("\tFile menu created successfully.")

    # Show the create command window
    def createCommand(self):
        self.createCommandWindow = CreateCommandApp(tk.Tk(), self.COMMANDS, None, "", lambda: self.populateCommandMenu())
        self.createCommandWindow.run()

    # Show the open command type dialog
    def loadCommandType(self):
        # Prompt user for file to load
        f = filedialog.askopenfile(mode='r', defaultextension='.csv')

        # If file is not empty (aka it exists)
        if f is not None:
            # Extract name from path string
            name = f.name.split('/')
            name = name[len(name)-1].replace('.csv', '').replace('_', ' ').title()

            print("\tLoading %s commands..." % name)

            # Append new type to global self.COMMANDS array
            self.COMMANDS.append(CommandType(name=name, path=f.name, commands=[]))

            # For each line in the file, create a command entry
            for line in f.readlines():
                split = line.split(',', 5)

                # If the first token starts with a parenthesis or bracket, re-split lines by first the 7 commas and
                # combine the 1st and 2nd tokens and the 3rd and 4th tokens into one each, then shift the array of tokens accordingly
                if split[0].startswith('[') or split[0].startswith('('):
                    split = line.split(',', 7)
                    split[0] = "%s, %s" % (split[0], split[1].replace(' ', '', 1))
                    split[1] = "%s, %s" % (split[2], split[3].replace(' ', '', 1))
                    split[2] = split[4]
                    split[3] = split[5]
                    split[4] = split[6]
                    split[5] = split[7]

                variables = []
                if split[2]:
                    c = 0
                    for v in split[2]:
                        low = split[3].split()[c].split('-')[0]

                        if isinstance(low, str) and low == '':
                            low = 0 - int(split[3].split()[c].split('-')[1])
                            high = int(split[3].split()[c].split('-')[2])
                        elif low == 'range':
                            low = -1000000
                            high = 1000000
                        else:
                            low = int(low)
                            high = int(split[3].split()[c].split('-')[1])

                        variables.append(Variable(symbol=v, low=low, high=high, currentValue=int(split[4].split()[c])))
                        c += 1

                self.getCommandType(name).getCommands().append(Command(name=split[0], command=split[1], variables=variables, description=split[5]))
                print("\t\t%s command loaded successfully." % self.getCommandType(name).getCommands()[-1].getName())

            print("\t%s commands loaded successfully." % name)

    # Load a program from a file
    def loadProgram(self):
        # TODO
        f = filedialog.askopenfile('r', defaultextension='.txt')

        if f:
            self.program = f.readlines()

            print(self.program)

            f.close()

    # Show the save command type as dialog
    def saveCommandType(self, As=True):
        if As == True:
            # Prompt user for a file to save
            f = filedialog.asksaveasfile(mode='w', defaultextension='.csv')
        else:
            # Use existing path
            f = open(self.getCommandType(self.selectedCommandType.get()).getPath(), 'w')

        # If file is opened successfully
        if f:
            print("\tSaving command type '%s'..." % self.selectedCommandType.get())

            # Write each command to the file
            for command in self.getCommandsOfType(self.selectedCommandType.get()):
                variables = []
                possibles = []
                values = []

                if command.getVariables():
                    for v in command.getVariables():
                        variables.append(v.getSymbol())
                        possibles.append(str(v.getLow()) + "-" + str(v.getHigh()))
                        values.append(str(v.getCurrentValue()))

                f.write("%s,%s,%s,%s,%s,%s\n" % (command.getName(), command.getCommand(), "".join(variables), " ".join(possibles), " ".join(values), command.getDescription().replace('\n', '')))
                print("\t\t%s saved successfully." % command.getName())

            print("\tCommand type '%s' saved as '%s' successfully." % (self.selectedCommandType.get(), f.name))

    # Create the edit menu for menu bar
    def createEditMenu(self):
        self.editMenu = tk.Menu(self.frame, tearoff=0)
        self.editMenu.add_command(label="Edit Command...", command=lambda: self.editCommand(self.getCurrentCommand()))
        self.editMenu.add_command(label="Rename Command Type...", command=self.renameCommandType)
        self.editMenu.add_separator()
        self.editMenu.add_command(label="Delete Command", command=lambda: self.deleteCommand(self.getCurrentCommand()))
        self.editMenu.add_command(label="Delete Command Type", command=self.deleteCommandType)
        self.editMenu.add_command(label="Reload Default Commands", command=self.reloadDefaults)

        # Add edit menu to menu bar
        self.menuBar.add_cascade(label="Edit", menu=self.editMenu)

    # Rename the current command type
    def renameCommandType(self):
        self.renameTypeWindow = RenameTypeApp(tk.Tk(), self.getCommandType(self.selectedCommandType.get()), self.doRename)
        self.renameTypeWindow.run()

    # Rename the currently selected command type to the specified value
    def doRename(self, newName):
        # Get current command type and new paths
        ctype = self.getCommandType(self.selectedCommandType.get())
        newPath = ctype.getPath().replace(str.lower(ctype.getName()).replace(' ', '_').replace('/', '_'), str.lower(newName).replace(' ', '_').replace('/', '_'))

        # Append new type to COMMANDS
        self.COMMANDS.append(CommandType(name=newName, path=newPath, commands=ctype.getCommands()))

        # Delete current command type
        self.deleteCommandType(prompt=False)

        # Repopulate command menus
        self.populateCommandTypeMenu()
        self.selectedCommandType.set(newName)
        self.populateCommandMenu()

        # Save to new version of the type
        self.saveCommandType(As=False)

        # Append new type to _types.csv
        file = open("commands%s_types.csv" % os.sep, 'a')
        file.write("%s,%s\n" % (newName, newPath.replace(os.sep, '->')))
        file.close()

    # Delete all commands in the current type and the type itself
    def deleteCommandType(self, prompt=True):
        sure = False

        if prompt == True:
            # Show messagebox alerting user they are about to delete a command type
            if messagebox.askyesno("Delete Command Type?", "Are you sure you would like to completely erase the command type '%s'?\nThis will delete all commands of this type and will be permanent." % self.selectedCommandType.get()):
                sure = True
        else:
            sure = True

        if sure == True:
            ctype = self.selectedCommandType.get()
            # Remove the file that containes this types commands
            os.remove(self.getPath(ctype))

            # Read the _types.csv file
            file = open("commands%s_types.csv" % os.sep, 'r')
            lines = file.readlines()
            file.close()

            # Remove type from _types.csv
            file = open("commands%s_types.csv" % os.sep, 'w')
            for line in lines:
                if not line.startswith(ctype):
                    file.write(line)
            file.close()

            # Get type index and delete type from self.COMMANDS array
            typeIndex, dummy = self.getCommandIndex(self.getCurrentCommand())
            del self.COMMANDS[typeIndex]

            # Repopulate menus
            self.populateCommandTypeMenu()
            self.selectedCommandType.set(self.commandTypeMenu['menu'].entrycget(0, 'label'))
            self.populateCommandMenu()

            print("\tCommand type '%s' has been removed successfully." % ctype)

    # Reload the default commands
    def reloadDefaults(self):
        # Set text to prompt user with
        text = "Are you sure you would like to reload the default commands? This will overwrite any changes you have made to the following default types, and cannot be undone:\n\nOperation Stored, Status Request, Input/Output, Looping/Branching, Motor, Pausing, Set"

        # Display messagebox to ask user if they are sure they want to load defaults
        if messagebox.askyesno("Reload Defaults?", text):
            print("\tReloading default commands...")

            # Remove existing version of default command types
            print("\t\tRemoving existing command type files...")
            if os.path.isdir("commands%simmediate" % os.sep) and os.path.exists("commands%simmediate" % os.sep):
                shutil.rmtree("commands%simmediate" % os.sep)
            if os.path.isdir("commands%sprogram_stored" % os.sep) and os.path.exists("commands%sprogram_stored" % os.sep):
                shutil.rmtree("commands%sprogram_stored" % os.sep)
            if os.path.isfile("commands%sset.csv" % os.sep):
                os.remove("commands%sset.csv" % os.sep)

            # Copy default files to commands directory
            print("\t\tCopying default files...")
            shutil.copytree("commands%s_defaults%simmediate" % (os.sep, os.sep), "commands%simmediate" % os.sep)
            shutil.copytree("commands%s_defaults%sprogram_stored" % (os.sep, os.sep), "commands%sprogram_stored" % os.sep)
            shutil.copyfile("commands%s_defaults%sset.csv" % (os.sep, os.sep), "commands%sset.csv" % os.sep)

            # If there is not a custom file, copy the one from defaults
            if not os.path.isfile("commands%scustom.csv" % os.sep):
                shutil.copyfile("commands%s_defaults%scustom.csv" % (os.sep, os.sep), "commands%scustom.csv" % os.sep)

            # Open the current and default types files and compare them
            file = open("commands%s_defaults%s_types.csv" % (os.sep, os.sep), 'r')
            defTypes = file.readlines()
            file.close()

            file = open("commands%s_types.csv" % os.sep, 'r')
            types = file.readlines()
            file.close()

            # For each type in the default that is not in the current types file, add it to the current types file
            for ctype in defTypes:
                if not ctype in types:
                    file = open("commands%s_types.csv" % os.sep, 'a')
                    file.write(ctype)
                    file.close()

            # Clear current commands and reload from _types.csv
            self.loadCommands()
            self.populateCommandTypeMenu()
            self.selectedCommandType.set(self.commandTypeMenu['menu'].entrycget(0, 'label'))
            self.populateCommandMenu()

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

        # For each command type object in self.COMMANDS, check the name and place it in the appropriate menu
        for ctype in self.COMMANDS:
            # For first two types, place is immediate menu
            if ctype.getName() == "Operation Stored" or ctype.getName() == "Status Request":
                tempMenu = self.immediateMenu
            # For next four types, place in program stored menu
            elif ctype.getName() == "Motor" or ctype.getName() == "Looping/Branching" or ctype.getName() == "Pausing" or ctype.getName() == "Input/Output":
                tempMenu = self.programStoredMenu
            # For all other types, place directly in commands menu, adding a separator before first other command type
            else:
                tempMenu = self.commandsMenu
                if ctype.getName() == "Custom":
                    tempMenu.add_separator()

            # Add the current command type to the selected menu
            tempMenu.add_command(label=ctype.getName(), command=lambda value=ctype.getName():self.showCommands(value))

            print("\t\t%s help option loaded successfully." % ctype.getName())

    # Display the commands dialog window
    def showCommands(self, ctype):
        self.createInfoWindow = ShowInfoApp(tk.Tk(), ctype, self.getCommandsOfType(ctype))
        self.createInfoWindow.run()

    # Display messagebox with information about this application
    def showAbout(self):
        messagebox.showinfo("About This Motor Controller", "This controller was written by Ian Tait for the Physics Department of the University of Kansas for the purpose of programming the VXM motor controller. This project is for a capstone class proctored by Dr. Graham Wilson.")

    # Run the application
    def run(self):
        self.mainloop()
