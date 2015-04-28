# Import messagebox to show errors
from tkinter import messagebox

# Import local libraries
from lib import command, variable
Command = command.Command
Variable = variable.Variable

# Class to store all necessary information for a VXM program
class Program():
    # Constructor function for a program
    def __init__(self, master=None, number=0, commands=None):
        # Verify that the number argument is an integer
        try:
            assert(isinstance(number, int))
        except AssertionError:
            print("Error: 'number' argument of Program must be an integer.")
            return

        self.number = number

        # Verify that the commands argument is a list
        if commands is not None:
            try:
                assert(isinstance(commands, list))
            except AssertionError:
                print("Error: 'commands' argument of Program must be a list.")
                return

        self.rawCommands = commands

        # If a master is defined, store it as global variable
        if master:
            self.master = master

        # Initialize compiledProgram global variable
        self.compiledProgram = ""

        # If commands are preset, attempt to compile them
        if self.rawCommands:
            self.compile()

    # Get the program number
    def getNumber(self):
        return self.number

    # Get the list of raw (unverified) program commands
    def getRawCommands(self):
        return self.rawCommands

    # Set get the compiled program text
    def getCompiledProgram(self):
        return self.compiledProgram

    # Set the program number
    def setNumber(self, n):
        self.number = n

    # Set the list of raw (unverified) program commands
    def setRawCommands(self, c):
        try:
            assert(isinstance(c, list))
        except AssertionError:
            print("Error: Argument of setRawCommands must be a list.")
            return

        self.rawCommands = c

    # Clear all commands and the compiled program
    def clear(self):
        self.rawCommands = None
        self.compiledProgram = ""

    # Add a command to the rawCommands list
    def addCommand(self, command):
        if self.rawCommands is None:
            self.rawCommands = []

        try:
            assert(isinstance(command, str))
        except AssertionError:
            print("Error: argument of addCommand must be a string.")
            return

        if self.rawCommands and self.rawCommands[-1] == "Q":
            self.rawCommands.remove('Q')
            self.rawCommands.append(command)
        else:
            self.rawCommands.append(command)

    # Compile the raw commands into a program
    def compile(self):
        if self.rawCommands is not None:
            # Clear the compiled program
            self.compiledProgram = ""

            # If commands list in not empty
            if self.rawCommands:
                # Add enable online mode, program clear/selection command, and quit online mode commands
                if self.rawCommands[0] != 'E':
                    self.rawCommands.insert(0, 'E')
                if self.rawCommands[-1] != 'Q':
                    self.rawCommands.append('Q')
                if self.rawCommands[1] != "PM-" + str(self.number):
                    self.rawCommands.insert(1, "PM-" + str(self.number))

            # Iterate through all raw commands
            for c in self.rawCommands:
                # Verify that the command syntax is correct (ie parenthesis are complete and in the correct positions)
                if c.__contains__('(') and not c.__contains__(')'):
                    print("Syntax Error in command %s. No terminating parenthesis." % c)
                    messagebox.showerror("Syntax Error", "No terminating parenthesis in command %s." % c)
                    self.compiledProgram = ""
                    return
                elif c.__contains__(')') and not c.__contains__('('):
                    print("Syntax Error in command %s. Terminating parenthesis without opening first." % c)
                    messagebox.showerror("Syntax Error", "Terminating parenthesis without opening first in command %s." % c)
                    self.compiledProgram = ""
                    return
                elif c.__contains__(')') and not c.endswith(')'):
                    print("Syntax Error: In command %s, text was found after parenthesis." % c)
                    messagebox.showerror("Syntax Error", "Text was found after parenthesis in command %s." % c)
                    self.compiledProgram = ""
                    return
                # If there are no problems with syntax, attempt to add the command to the compiled program
                else:
                    # If the command is a function, get the name and arguments
                    if c.__contains__('(') and not c.startswith('('):
                        name = c[:-1].split('(')[0]
                        args = self.parseArguments(c[:-1].split('(')[1].split(','))

                        command = self.master.getCommand(name)

                        # If there is not a command with the name provided, throw an error
                        if command is None:
                            print("Function Error: Cannot call a command '%s' as function because this command does not exist." % name)
                            messagebox.showerror("Function Error: %s" % name, "You cannot call a command by name as a function if the command name does not exist. Please create a command with the name '%s'" % name)
                            self.compiledProgram = ""
                            return

                        if args:
                            count = 0
                            for arg in args:
                                try:
                                    command.getVariable(count).setCurrentValue(arg)
                                    command.getVariable(count).setEntryValue(arg)
                                except IndexError:
                                    print("Index Error: You provided too many arguments in command %s. There are %i variables for this command." % (c, count+1))
                                    messagebox.showerror("Index Error", "You have provided too many arguments for the command '%s'. There are %i variables available for this command." % (c, count+1))
                                    self.compiledProgram = ""
                                    return
                                count += 1

                            self.compiledProgram += "," + command.getCommand()
                        else:
                            self.compiledProgram += "," + command.getCommand()

                        print("\t\t\t%s" % name, args)
                    # If the command is not a function, add the command as is to the compiled program
                    else:
                        self.compiledProgram += "," + c
                        print("\t\t\t%s" % c)

            self.compiledProgram = self.compiledProgram[1:]

    # Parse a command's arguments and return a list containing the arguent values in order
    def parseArguments(self, arguments):
        # Initialize return list
        args = []

        # Iterate through arguments
        for arg in arguments:
            # If the argument isn't empty
            if arg:
                # If the argument is an integer, append the integer value to the arguments list
                if self.isAnInt(arg.strip()):
                    args.append(int(arg.strip()))
                # Else strip quotes and append string to the arguments list
                else:
                    arg = arg.strip().replace("'", '').replace('"', '')
                    args.append(arg)
        # Return arguments in an organized list
        return args

    # Determine if the string represents an integer
    def isAnInt(self, string):
        try:
            int(string)
            return True
        except ValueError:
            return False
