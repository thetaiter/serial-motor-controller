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

    # Set command frame
    def setFrame(self, f):
        self.frame = f

    # Set get command name
    def getName(self):
        return self.name

    # Get the raw command text
    def getCommandRaw(self):
        return self.command

    # Get the compiled command
    def getCommand(self):
        ret = "" + self.command

        for v in self.variables:
            if v.getEntryValue():
                ret = ret.replace(v.getSymbol(), v.getEntryValue())
            else:
                 ret = ret.replace(v.getSymbol(), v.getCurrentValue())

        return ret

    # Get command variables
    def getVariables(self):
        return self.variables

    # Get command variable by index or name
    def getVariable(self, index=0):
        if isinstance(index, int):
            return self.variables[index]
        elif isinstance(index, str):
            for v in self.variables:
                if v.symbol == index:
                    return v
        else:
            print("\nGet variable failed, index=%s is invalid.\n" % index)

    # Get number of variables
    def numVariables(self):
        return len(self.variables)

    # Get command description
    def getDescription(self):
        return self.description

    # Get command frame
    def getFrame(self):
        return self.frame
