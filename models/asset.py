class Asset:
    """
    Base class representing a financial asset.
    """

    def __init__(self, symbol, name, quantity=1):
        self.symbol = symbol.upper()
        self.name = name
        self.quantity = quantity

    def display_info(self):
        return f"{self.symbol} - {self.name} | Quantity: {self.quantity:g}"
