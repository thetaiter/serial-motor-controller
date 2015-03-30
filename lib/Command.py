class Command():
    # Constructor
    def __init__(self, name='New Command', command='command_x', variables=None, description='Description', frame=None):
        # Set name and command
        self.name = name
        self.command = command

        # Assert that variables is a list
        try:
            assert(isinstance(variables, list))
        except AssertionError:
            print("Error: Variables attribute of Command must be a list.")
            return

        # Assert that variables match characters in command string
        try:
            for v in variables:
                assert(self.command.__contains__(v.symbol))
        except AssertionError:
            print("Error: Variables entered must have symbols that match characters in the command string.")
            return

        # Set variables, description and frame
        self.variables = variables
        self.description = description
        self.frame = frame

    # Set command name
    def setName(self, n):
        self.name = n

    # Set command command
    def setCommand(self, c):
        self.command = c

    # Set command variables
    def setVariables(self, vars):
        # Assert vars is a list
        try:
            assert(isinstance(vars, list))
        except AssertionError:
            print("Error: Variables attribute of Command must be a list.")
            return

        # Assert that chars in vars are in command string
        try:
            for v in vars:
                assert(self.command.__contains__(v.symbol))
        except AssertionError:
            print("Error: Variables entered must have symbols that match characters in the command string.")
            return

        self.variables = vars

    # Set command description
    def setDescription(self, d):
        self.description = d

    # Set get command name
    def getName(self):
        return self.name

    # Get command command
    def getCommand(self):
        return self.command

    # Get command variables
    def getVariables(self):
        return self.variables

    # Get command variable by index
    def getVariable(self, index=0):
        return self.variables[index]

    # Get number of variables
    def numVariables(self):
        return len(self.variables)

    # Get command description
    def getDescription(self):
        return self.description