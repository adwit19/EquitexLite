from models.asset import Asset


class Portfolio:
    """
    Represents a user's portfolio of assets.
    """

    def __init__(self):
        self._assets = []

    def add_asset(self, asset):
        if not isinstance(asset, Asset):
            raise TypeError("Portfolio can only store Asset objects.")
        self._assets.append(asset)

    def remove_asset(self, symbol):
        symbol = symbol.upper()

        for asset in self._assets:
            if asset.symbol == symbol:
                self._assets.remove(asset)
                return True

        return False

    def display_assets(self):
        return [asset.display_info() for asset in self._assets]

    def get_total_assets(self):
        return len(self._assets)

    def get_assets(self):
        return self._assets