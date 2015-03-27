class Variable():
    def __init__(self, symbol='x', low=0, high=10, currentValue=5, mid=5):
        self.symbol = symbol

        try:
            assert(low <= high)
        except AssertionError:
            print("Error: The low value must be equal to or less than the high value.")
            return

        self.low = low
        self.mid = mid
        self.high = high

        try:
            assert(currentValue >= low)
            assert(currentValue <= high)
            self.currentValue = currentValue
        except AssertionError:
            print("Error: Variable value error, currentValue should be between low and high (inclusive).")
            self.currentValue = low

    def setSymbol(self, sym):
        self.symbol = sym

    def setLow(self, l):
        self.low = l

    def setHigh(self, h):
        self.high = h

    def setCurrentValue(self, c):
        try:
            assert(c >= self.low)
            assert(c <= self.high)
        except AssertionError:
            print("\nError: Variable value error, currentValue should be between low and high (inclusive).")
            return

        self.currentValue = c

    def getSymbol(self):
        return self.symbol

    def getLow(self):
        return self.low

    def getHigh(self):
        return self.high

    def getLowAndHigh(self):
        return self.low, self.high

    def getCurrentValue(self):
        return self.currentValue