class Command():
    def __init__(self, name='New Command', command='command_x', variables=None, description='Description', frame=None):
        self.name = name
        self.command = command

        try:
            assert(isinstance(variables, list))
        except AssertionError:
            print("Error: Variables attribute of Command must be a list.")
            return

        try:
            for v in variables:
                assert(self.command.__contains__(v.symbol))
        except AssertionError:
            print("Error: Variables entered must have symbols that match characters in the command string.")
            return

        self.variables = variables
        self.description = description
        self.frame = frame

    def setName(self, n):
        self.name = n

    def setCommand(self, c):
        self.command = c

    def setVariables(self, vars):
        try:
            assert(isinstance(vars, list))
        except AssertionError:
            print("Error: Variables attribute of Command must be a list.")
            return

        try:
            for v in vars:
                assert(self.command.__contains__(v.symbol))
        except AssertionError:
            print("Error: Variables entered must have symbols that match characters in the command string.")
            return

        self.variables = vars

    def setDescription(self, d):
        self.description = d

    def getName(self):
        return self.name

    def getCommand(self):
        return self.command

    def getVariables(self):
        return self.variables

    def getVariable(self, index=0):
        return self.variables[index]

    def getDescription(self):
        return self.description