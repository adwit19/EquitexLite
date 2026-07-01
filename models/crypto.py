from models.asset import Asset


class Crypto(Asset):

    def __init__(self, symbol, name):
        super().__init__(symbol, name)