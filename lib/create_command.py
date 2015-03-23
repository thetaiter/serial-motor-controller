# Import built-in libraries
from collections import namedtuple
import sys
import re

# Import 3rd party libraries
import tkinter as tk
from tkinter import messagebox

# Set path delimiter
PATH_DELIMITER = ""

if sys.platform.startswith('win'):
    PATH_DELIMITER = "\\"
else:
    PATH_DELIMITER = "/"

# Set Global Variables
WINDOW_SIZE = [300, 245]
TITLE = "Create Command"
HELP = {
    "Name": "This is the name of your new command. It will be added to the list of custom commands.",
    "Command": "This is the command entry for your new command. If any characters in the command are meant to take adjustable values, place those characters in a string in the variables entry. For example, if your command is \"move_motorM_x\" and you want \"M\" to represent which motor to move, and \"x\" to represent the number of steps to move, place \"Mx\" or \"xM\" in the variables entry.",
    "Variables": "This is the entry for all the variables that you intend to adjust. Do not put spaces or any other characters between them. Leave blank if you do not wish to use variables in this command.",
    "Possible": "This is the entry for all possible values that your variables can take. For each variable repespectively, you must have a set of possible values. The possible values for each of your variables will need to be space delimited, and must be a range delimited by '-'.  For example: if you have two variables 'xM' and x can take values 1 to 100, and M can take values 0 to 4, you would type '1-100 0-4' in the possible values entry box.",
    "Values": "This is the entry for a space delimited list of inital values for the variables you entered. They will be assigned in the order you entered the variables in the variables entry. Leave blank if you did not enter any variables.",
    "Description": "This is the entry for a description of what the command does.",
    "Type": "This is the type of command you want to create. Your command will be organized in menus and things based on it's type. The default new command type is 'Custom'.",
    "NoEntry": "There is no help entry for this item yet."
}

# Custom structures for Command and Command Type
Command = namedtuple("Command", ["name", "command", "variables", "possible", "values", "description"])
CommandType = namedtuple("CommandType", ["name", "path", "commands"])

# Class for the create command app
class CreateCommandApp(tk.Frame):
    # Constructor Initialization function
    def __init__(self, master, commands, command=None, type="", callback=None):
        # Initialize the TK frame
        tk.Frame.__init__(self, master)

        # Pull commands into app
        self.commands = commands

        self.saved = 'false'
        self.edit = 'false'

        # Initialize command
        if command is None:
            self.command = Command("", "", "", "", "", "")
        else:
            self.command = command
            self.edit = 'true'
            self.type = type

        self.callback = callback

        # Setup the window
        self.setupWindow()

        # Set initial status and saved values
        self.status = 'initiated'

    # Setup the tkinter window and frame
    def setupWindow(self):
        # Setup window geometry, position and title
        self.xPos, self.yPos = self.calculateWindowOffset()
        self.master.geometry("%dx%d%+d%+d" % (WINDOW_SIZE[0], WINDOW_SIZE[1], self.xPos, self.yPos))
        self.master.resizable(width='false', height='false')
        self.master.title(TITLE)

        # Create frame for objects in window
        self.frame = tk.Frame(self.master)
        self.frame.place(x=0, y=0, width=WINDOW_SIZE[0], height=WINDOW_SIZE[1])

        # Create and place the name label, entry and help button
        self.nameLabel = tk.Label(self.frame, text="Name:")
        self.nameLabel.place(x=5, y=10, width=40)
        self.nameEntry = tk.Entry(self.frame)
        self.nameEntry.place(x=55, y=10, width=WINDOW_SIZE[0]-80)
        self.nameButton = tk.Button(self.frame, text='?', command=lambda: self.showHelp('Name'))
        self.nameButton.place(x=WINDOW_SIZE[0]-20, y=9, width=15, height=20)

        # Create and place the command label, entry and help button
        self.commandLabel = tk.Label(self.frame, text="Command:")
        self.variablesButton = tk.Button(self.frame, text='?', command=lambda: self.showHelp('Variables'))
        self.variablesButton.place(x=WINDOW_SIZE[0]-20, y=59, width=15, height=20)

        # Create and place the possible values label, entry, and help button
        self.possibleLabel = tk.Label(self.frame, text="Poss. Values:")
        self.commandLabel.place(x=5, y=35, width=60)
        self.commandEntry = tk.Entry(self.frame)
        self.commandEntry.place(x=75, y=35, width=WINDOW_SIZE[0]-100)
        self.commandButton = tk.Button(self.frame, text='?', command=lambda: self.showHelp('Command'))
        self.commandButton.place(x=WINDOW_SIZE[0]-20, y=34, width=15, height=20)

        # Create and place the variables label, entry and help button
        self.variablesLabel = tk.Label(self.frame, text="Variables:")
        self.variablesLabel.place(x=5, y=60, width=55)
        self.variablesEntry = tk.Entry(self.frame)
        self.variablesEntry.place(x=70, y=60, width=WINDOW_SIZE[0]-95)
        self.possibleLabel.place(x=5, y=85, width=75)
        self.possibleEntry = tk.Entry(self.frame)
        self.possibleEntry.place(x=85, y=85, width=WINDOW_SIZE[0]-110)
        self.possibleButton = tk.Button(self.frame, text='?', command=lambda: self.showHelp('Possible'))
        self.possibleButton.place(x=WINDOW_SIZE[0]-20, y=84, width=15, height=20)

        # Create and place the values label, entry, and help button
        self.valuesLabel = tk.Label(self.frame, text="Values:")
        self.valuesLabel.place(x=5, y=110, width=45)
        self.valuesEntry = tk.Entry(self.frame)
        self.valuesEntry.place(x=60, y=110, width=WINDOW_SIZE[0]-85)
        self.valuesButton = tk.Button(self.frame, text='?', command=lambda: self.showHelp('Values'))
        self.valuesButton.place(x=WINDOW_SIZE[0]-20, y=109, width=15, height=20)

        # Create and place the description label, entry and help button
        self.descriptionLabel = tk.Label(self.frame, text="Description:")
        self.descriptionLabel.place(x=5, y=135, width=65)
        self.descriptionEntry = tk.Entry(self.frame)
        self.descriptionEntry.place(x=80, y=135, width=WINDOW_SIZE[0]-105)
        self.descriptionButton = tk.Button(self.frame, text='?', command=lambda: self.showHelp('Description'))
        self.descriptionButton.place(x=WINDOW_SIZE[0]-20, y=134, width=15, height=20)

        # Create and place the command type label, option menu, and help button
        self.typeLabel = tk.Label(self.frame, text="Type:")
        self.typeLabel.place(x=5, y=161, width=35)
        self.selectedType = tk.StringVar(self.master)
        self.typeMenu = tk.OptionMenu(self.frame, self.selectedType, ())
        self.typeMenu.place(x=45, y=156, width=WINDOW_SIZE[0]-70)
        self.typeButton = tk.Button(self.frame, text='?', command=lambda: self.showHelp('Type'))
        self.typeButton.place(x=WINDOW_SIZE[0]-20, y=161, width=15, height=20)

        # Create and place the type name label and entry
        self.typeTextLabel = tk.Label(self.frame, text="Type Name:")
        self.typeTextLabel.place(x=5, y=190, width=65)
        self.typeText = tk.StringVar(self.master)
        self.typeTextBox = tk.Entry(self.frame, textvariable=self.typeText, state='readonly')
        self.typeTextBox.place(x=75, y=190, width=WINDOW_SIZE[0]-80)

        # Populate the type menu
        self.populateTypeMenu()

        # Create and place the save button
        self.saveButton = tk.Button(self.frame, text='Save Command', command=self.checkAndSave)
        self.saveButton.place(x=(WINDOW_SIZE[0]/2)-150/2, y=WINDOW_SIZE[1]-30, width=150)

        if self.edit == 'true':
            self.nameEntry.insert(0, self.command.name)
            self.commandEntry.insert(0, self.command.command)
            self.variablesEntry.insert(0, self.command.variables)
            self.possibleEntry.insert(0, str(self.command.possible).replace('[', '').replace(']', ''))
            self.valuesEntry.insert(0, self.command.values)
            self.descriptionEntry.insert(0, self.command.description)
            self.selectedType.set(self.type)

        # Set method for when user clicks the window's 'x' button
        self.master.protocol("WM_DELETE_WINDOW", self.quitApp)

    # Calculate window position on screen
    def calculateWindowOffset(self):
        # Calculate the x position of the top right corner of the window that is necessary to center it horizontally
        x = (self.master.winfo_screenwidth() / 2) - (WINDOW_SIZE[0] / 2)

        # Calculate the y position of the top right corner of the window that is necessary to center it vertically
        y = (self.master.winfo_screenheight() / 2) - (WINDOW_SIZE[1] / 2)

        return x, y

    # Populate command type menu
    def populateTypeMenu(self):
        # For each type, add an option to the command type menu
        for type in self.commands:
            self.typeMenu['menu'].add_command(label=type.name, command=lambda name=type.name: self.updateType(name))

        # Add an option to adda new type and delete first empty object
        self.typeMenu['menu'].add_command(label="New Type...", command=lambda: self.updateType("New Type..."))
        self.typeMenu['menu'].delete(0)

        # Set default command type to custom
        self.selectedType.set("Custom")

    # Update the command type.
    def updateType(self, typeName):
        # Set current type
        self.selectedType.set(typeName)

        # If new type is selected, enable to type name entry else clear it and disable it
        if typeName == "New Type...":
            self.typeTextBox.config(state='normal')
        else:
            self.typeTextBox.delete(0, 'end')
            self.typeTextBox.config(state='readonly')

    # Get the current command type
    def getCommandType(self, ctype):
        count = 0
        for commandType in self.commands:
            if commandType.name == ctype:
                return self.commands[count]
            count += 1

    # Display a messabgebox with the help entry for the given option
    def showHelp(self, entry):
        # If there is an entry, display it else display no entry
        if HELP[entry]:
            messagebox.showinfo(entry, HELP[entry])
        else:
            messagebox.showinfo(entry, HELP["NoEntry"])

        # Resume focus on create command window
        self.master.focus_force()

    # Check for changes and save if there are any
    def checkAndSave(self):
        if self.checkForChanges() == 'true':
            self.saved = 'false'
            self.saveCommand()

    # Save the current comand entry
    def saveCommand(self):
        # If the entries are valid and not saved yet, save the command else do not save
        if self.verifyEntries() == 'true' and self.saved == 'false':
            if self.edit == 'true':
                self.deleteCommand()

            # Import entries into self variable
            self.command = Command(self.nameEntry.get(), self.commandEntry.get(), self.variablesEntry.get(), self.possibleEntry.get(), self.valuesEntry.get(), self.descriptionEntry.get())

            # If there is text in the type name entry, create a new entry in the _types.csv file and add to commands array, else just update existing command type entry
            if self.typeText.get():
                # Set the path for the new type
                path = "commands%s%s.csv" % (PATH_DELIMITER, str.lower(self.typeText.get().replace(" ", "_")))

                # Update _types.csv
                with open("commands%s_types.csv" % PATH_DELIMITER, 'a') as file:
                    file.write("%s,%s\n" % (self.typeText.get(), path))
                    file.close()

                # Append type to commands
                self.commands.append(CommandType(name=self.typeText.get(), path=path, commands=[self.command]))
            else:
                # Update existing command type entry
                path = self.getCommandType(self.selectedType.get()).path
                self.getCommandType(self.selectedType.get()).commands.append(self.command)

            # Open command type file and add new command
            with open(path, 'a') as file:
                file.write("%s,%s,%s,[%s],%s,%s\n" % (self.command.name, self.command.command, self.command.variables, self.command.possible, self.command.values, self.command.description.replace('\n', '')))
                file.close()

            # Set saved to true
            self.saved = 'true'

            # Close the create command window
            self.quitApp()
        else:
            # Resume focus on create command window
            self.master.focus_force()

    # Delete the specified command
    def deleteCommand(self):
        # Get indexes of type and command
        typeIndex, comIndex = self.getCommandIndex()

        # If command exists, delete it from the list of commands
        if typeIndex != -1 and comIndex != -1:
            del(self.commands[typeIndex].commands[comIndex])

        # Read file where command originated from
        file = open(self.getPath(self.type), 'r')
        lines = file.readlines()
        file.close()

        # Overwrite the file with all entries except desired command to delete
        with open(self.getPath(self.type), 'w') as file:
            for line in lines:
                if not line.startswith(self.command.name):
                    file.write(line)
            file.close()

    # Get the index of the command's type in the global COMMANDS array and the index of the command within the commands array of that type
    def getCommandIndex(self):
        # For each type in COMMANDS, iterate through commands
        typeCount = 0
        for ctype in self.commands:
            comCount = 0
            for command in ctype.commands:
                # If command name is same as desired command, return index of type and command
                if command.name == self.command.name:
                    return typeCount, comCount
                # Incrememnt command counter
                comCount += 1
            # Incrememnt type counter
            typeCount += 1

        # If command was not found, return negative values
        return -1, -1

    # Get the file path of the commands that are of the specified type
    def getPath(self, ctype):
        for ct in self.commands:
            if ct.name == ctype:
                return ct.path

    # Find specific chars in a string
    def findCharsInString(self, string, chars):
        # Create return object
        ret = {}

        # For each char to search in the string for
        for c in chars:
            # For each char in the string
            for char in string:
                # If the curretn string char equals current search char
                if c == char:
                    # If the char has already been found once, increment count for that char, else create attribute and set count to 1
                    if ret.get(c):
                        ret[c] += 1
                    else:
                        ret[c] = 1

        # Return JSON object with counts
        return ret

    # Verify current entries
    def verifyEntries(self):
        # If nothing is in name entry, display messagebox and return false
        if not self.nameEntry.get() or not self.nameEntry.get().replace(" ", ""):
            self.nameEntry.delete(0, 'end')
            messagebox.showerror("No Name", "Error: You must enter a name for this command.")
            return 'false'

        # Strip spaces off beginning and end of name entry
        stripped = " ".join(self.nameEntry.get().split())
        self.nameEntry.delete(0, 'end')
        self.nameEntry.insert(0, stripped)

        # If nothing is in command entry, display messagebox and return false
        if not self.commandEntry.get() or not self.commandEntry.get().replace(" ", ""):
            self.commandEntry.delete(0, 'end')
            messagebox.showerror("No Command", "Error: You must enter a command.")
            return 'false'

        # Strip spaces off beginning and end of command entry
        stripped = self.commandEntry.get().strip()
        self.commandEntry.delete(0, 'end')
        self.commandEntry.insert(0, stripped)

        # If variables exist but no possible values are entered, display messagebox and return false
        if (self.variablesEntry.get() and self.variablesEntry.get().replace(" ", "")) and (not self.possibleEntry.get() or not self.possibleEntry.get().replace(" ", "")):
            self.possibleEntry.delete(0, 'end')
            messagebox.showerror("No Possible Values", "Error: If you enter a variable, you must enter possible values for each variable.")
            return 'false'

        # If variables exist but no values are entered, display messagebox and return false
        if (self.variablesEntry.get() and self.variablesEntry.get().replace(" ", "")) and (not self.valuesEntry.get() or not self.valuesEntry.get().replace(" ", "")):
            self.valuesEntry.delete(0, 'end')
            messagebox.showerror("No Values", "Error: If you enter a variable, you must enter an initial value for it.")
            return 'false'

        # If values or possible values are entered and no variables are entered, display  messagebox and return false
        if (not self.variablesEntry.get() or not self.variablesEntry.get().replace(" ", "")) and ((self.valuesEntry.get() and self.valuesEntry.get().replace(" ", "")) or (self.possibleEntry.get() and self.valuesEntry.get().replace(" ", ""))):
            self.variablesEntry.delete(0, 'end')
            messagebox.showerror("No Variables", "Error: You mest enter a valid variable in order to set initial values.")
            return 'false'

        # If previous tests have passed and there are variables present, verify that values and possible values are valid
        if self.variablesEntry.get():
            # Strip spaces off beginning and end of variables, possible values, and values
            stripped = self.variablesEntry.get().replace(" ", "")
            self.variablesEntry.delete(0, 'end')
            self.variablesEntry.insert(0, stripped)
            stripped = self.possibleEntry.get().strip()
            self.possibleEntry.delete(0, 'end')
            self.possibleEntry.insert(0, stripped)
            stripped = self.valuesEntry.get().strip()
            self.valuesEntry.delete(0, 'end')
            self.valuesEntry.insert(0, stripped)

            # If all variables provided are not found at least once within the command string, display messagebox and return false
            if len(self.findCharsInString(self.commandEntry.get(), self.variablesEntry.get()).keys()) != len(self.variablesEntry.get()):
                messagebox.showerror("Invalid Variables", "One or more of the variables you entered are not in the command string.")
                return 'false'

            # If the number of variables is not equal to the number of possible values provided, display messagebox and return false
            if len(self.variablesEntry.get()) != len(self.possibleEntry.get().split()):
                messagebox.showerror("Invalid Possible Values", "The number of possible values you have entered is not equal to the number of variables you entered.")
                return 'false'

            # Verify that all possible values are of the proper format for a ranege of values
            for possible in self.possibleEntry.get().split():
                # Create regular expression
                regex = re.compile('[0-9]*-[0-9]*')

                # Check if range matches regular expression, if not display messagebox and return false
                if regex.match(possible) is None:
                    messagebox.showerror("Invalid Possible Value", "The possible value '%s' that you entered is of the incorrect format. It must be of the format 'L-H' where 'L' is the lower bound value and H is the upper bound value." % possible)
                    return 'false'

            # If the number of variables is not equal to the number of values provided, display messagebox and return false
            if len(self.variablesEntry.get()) != len(self.valuesEntry.get().split()):
                messagebox.showerror("Invalid Values", "The number of values you have entered is not equal to the number of variables you entered.")
                return 'false'

            # Verify that values provided are within the range of possible values provided
            possibles = self.possibleEntry.get().split()
            count = 0

            for value in self.valuesEntry.get().split():
                # Convert lower, upper limits and value it integers
                lower = int(possibles[count].split('-')[0])
                upper = int(possibles[count].split('-')[1])
                value = int(value)

                # Check if value is within lower and upper bounds. If not, display messagebox and return false
                if value < lower:
                    messagebox.showerror("Invalid value", "The value '%s' is invalid because it is below the range specified in possible values. The possible values you entered range from %s to %s." % (value, lower, upper))
                    return 'false'
                elif value > upper:
                    messagebox.showerror("Invalid value", "The value '%s' is invalid because it is above the range specified in possible values. The possible values you entered range from %s to %s." % (value, lower, upper))
                    return 'flase'

                # Increment counter
                count += 1

        #  If no description is entered, display messagebox and return false
        if not self.descriptionEntry.get() or not self.descriptionEntry.get().replace(" ", ""):
            self.descriptionEntry.delete(0, 'end')
            messagebox.showerror("No Description", "Error: You must enter a description for this command.")
            return 'false'

        # If New Type... is selected and no type name is entered, display messagebox and return false
        if self.selectedType.get() == "New Type...":
            if not self.typeText.get() or not self.typeText.get().replace(" ", ""):
                self.typeText.set("")
                messagebox.showerror("No Type", "Error: You must enter the name of your new type if you have 'New Type' selected.")
                return 'false'

            if self.getCommandType(self.typeText.get()) is not None:
                messagebox.showerror("Duplicate Name", "Error: The type name you have entered already exists.")
                return 'false'
        else:
            for command in self.getCommandType(self.selectedType.get()).commands:
                if self.nameEntry.get() == command.name:
                    messagebox.showerror("Duplicate Name", "Error: The command name you have entered already exists in this type. Please enter a new name to continue.")
                    return 'false'

        # If all validations pass, return true
        return 'true'

    # Check if changes have been made since last save attempt
    def checkForChanges(self):
        # Initialize values
        variables = ""
        possible = ""
        values = ""

        # Check if variables, possible values, and values are entered
        if self.variablesEntry.get():
           variables = self.variablesEntry.get()
        if self.possibleEntry.get():
            possible = self.possibleEntry.get()
        if self.valuesEntry.get():
            values = self.valuesEntry.get()

        # If nothing has changed, return false
        if self.command.name == self.nameEntry.get() and self.command.command == self.commandEntry.get() and self.command.variables == variables and self.command.possible == possible and self.command.values == values and self.command.description == self.descriptionEntry.get():
            return 'false'

        # If something has changed, return true
        return 'true'

    # Run the application
    def run(self):
        self.status = 'running'
        self.mainloop()

    # Close the application
    def quit(self):
        # Set app status to  destroyed
        self.status = 'destroyed'

        # Destroy the application
        self.master.destroy()

    # Quit the application
    def quitApp(self):
        # If the user would like to save teh command, command is saved, else command is not saved
        if self.saved == 'false' or self.checkForChanges() == 'true':
            if messagebox.askyesno("Save Command?", "Would you like to save this command?"):
                self.saveCommand()

        # Run the callback command
        self.callback()

        # Close the application
        self.quit()
