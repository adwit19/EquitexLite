class Asset:
    """
    Base class representing a financial asset.
    """

    def __init__(self, symbol, name, quantity=1, purchase_price=0.0):
        self.symbol = symbol.upper()
        self.name = name
        self.quantity = quantity
        self.purchase_price = float(purchase_price or 0.0)

        if self.purchase_price < 0:
            raise ValueError("Purchase price must be non-negative.")

    def display_info(self):
        return f"{self.symbol} - {self.name} | Quantity: {self.quantity:g}"
