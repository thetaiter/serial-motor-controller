class Variable():
    # Constructor
    def __init__(self, symbol='x', low=0, high=10, currentValue=5, mid=5):
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
    def setCurrentValue(self, c):
        try:
            assert(c >= self.low)
            assert(c <= self.high)
        except AssertionError:
            print("\nError: Variable value error, currentValue should be between low and high (inclusive).")
            return

        self.currentValue = c

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