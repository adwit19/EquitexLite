from models.asset import Asset


class Stock(Asset):

    def __init__(self, symbol, name, quantity=1, purchase_price=0.0):
        super().__init__(symbol, name, quantity, purchase_price)
