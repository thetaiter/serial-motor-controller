class Variable():
    # Constructor
    def __init__(self, symbol='x', low=0, high=10, currentValue=5, entry=None):
        # Set symbol
        self.symbol = symbol

        # Assert that low is less than or equal to high
        try:
            assert(low <= high)
        except AssertionError:
            print("Error: The low value must be equal to or less than the high value.")
            return

        # Set low and high values
        self.low = low
        self.high = high

        # Assert that the current values is between the low and high
        try:
            assert(currentValue >= low)
            assert(currentValue <= high)
            self.currentValue = currentValue
        except AssertionError:
            print("Error: Variable value error, currentValue should be between low and high (inclusive).")
            self.currentValue = low

        self.entry = entry

        if self.entry:
            self.entry.delete(0, 'end')
            self.entry.insert(0, self.currentValue)

    # Set variable symbol
    def setSymbol(self, sym):
        self.symbol = sym

    # Set variable low value
    def setLow(self, l):
        self.low = l

    # Set variable high value
    def setHigh(self, h):
        self.high = h

    # Set variable current value
    def setCurrentValue(self, c=None):
        if c is None:
            c = int(self.entry.get())

        try:
            assert(c >= self.low)
            assert(c <= self.high)
        except AssertionError:
            print("\nError: Variable value error, currentValue should be between low and high (inclusive).")
            return

        self.currentValue = c

    # Set variable entry
    def setEntry(self, e):
        self.entry = e

    # Set variable entry value
    def setEntryValue(self, val):
        self.entry.delete(0, 'end')
        self.entry.insert(0, val)

    # Get variable symbol
    def getSymbol(self):
        return self.symbol

    # Get variable low value
    def getLow(self):
        return self.low

    # Get variable high value
    def getHigh(self):
        return self.high

    # Get low and high value together
    def getLowAndHigh(self):
        return self.low, self.high

    # Get variable current value
    def getCurrentValue(self):
        return self.currentValue

    # Get the variable entry
    def getEntry(self):
        if self.entry:
            return self.entry

    # Get the variable's entry value
    def getEntryValue(self):
        if self.entry:
            return self.entry.get()
