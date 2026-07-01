class Asset:
    """
    Base class representing a financial asset.
    """

    def __init__(self, symbol, name):
        self.symbol = symbol.upper()
        self.name = name

    def display_info(self):
        return f"{self.symbol} - {self.name}"