class CommandType():
    # Constructor
    def __init__(self, name='New Type', path='', commands=None):
        # Set name and path
        self.name = name
        self.path = path

        # If a command is passed in, assert that it is a list
        if commands is not None:
            try:
                assert(isinstance(commands, list))
            except AssertionError:
                print("Error: commands must be a list.")
                return

        # Set commands
        self.commands = commands

    # Set command type name
    def setName(self, n):
        self.name = n

    # Set command type path
    def setPath(self, p):
        self.path = p

    # Set commands array
    def setCommands(self, c):
        # Assert that c is a list
        try:
            assert(isinstance(c, list))
        except AssertionError:
            print("Error: commands must be a list.")
            return

        self.commands = c

    # Get command type name
    def getName(self):
        return self.name

    # Get command type path
    def getPath(self):
        return self.path

    # Get list of commands
    def getCommands(self):
        return self.commands

    # Get command by index
    def getCommand(self, index):
        if self.commands is not None:
            if isinstance(index, int):
                return self.commands[index]
            elif isinstance(index, str):
                for command in self.commands:
                    if command.name == index:
                        return command
        return None

    # Get number of commands
    def numCommands(self):
        if self.commands:
            return len(self.commands)
        return 0