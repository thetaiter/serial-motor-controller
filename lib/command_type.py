class CommandType():
    def __init__(self, name='New Type', path='', commands=None):
        self.name = name
        self.path = path

        if commands is not None:
            try:
                assert(isinstance(commands, list))
            except AssertionError:
                print("Error: commands must be a list.")
                return

        self.commands = commands

    def setName(self, n):
        self.name = n

    def setPath(self, p):
        self.path = p

    def setCommands(self, c):
        try:
            assert(isinstance(c, list))
        except AssertionError:
            print("Error: commands must be a list.")
            return

        self.commands = c

    def getName(self):
        return self.name

    def getPath(self):
        return self.path

    def getCommands(self):
        return self.commands

    def getCommand(self, index):
        return self.commands[index]

    def getCommandByName(self, name):
        for command in self.commands:
            if command.name == name:
                return command
