from models.asset import Asset
from services.api_manager import APIManager


class Portfolio:
    """
    Represents a user's portfolio of assets.
    """

    def __init__(self):
        self._assets = []

    def add_asset(self, asset):
        if not isinstance(asset, Asset):
            raise TypeError("Portfolio can only store Asset objects.")

        if self.update_quantity(asset.symbol, asset.quantity, asset.purchase_price):
            return False

        self._assets.append(asset)
        return True

    def update_quantity(self, symbol, quantity, purchase_price=None):
        symbol = symbol.upper()

        for asset in self._assets:
            if asset.symbol == symbol:
                if purchase_price is not None:
                    total_cost = asset.purchase_price * asset.quantity
                    added_cost = purchase_price * quantity
                    asset.quantity += quantity
                    asset.purchase_price = (
                        total_cost + added_cost
                    ) / asset.quantity
                else:
                    asset.quantity += quantity
                return True

        return False

    def remove_asset(self, symbol):
        symbol = symbol.upper()

        for asset in self._assets:
            if asset.symbol == symbol:
                self._assets.remove(asset)
                return True

        return False

    def display_assets(self):
        return [asset.display_info() for asset in self._assets]

    def calculate_total_value(self):
        valued_assets = []
        total_value = 0

        for asset in self._assets:
            try:
                stock_data = APIManager.get_stock_data(asset.symbol)
                market_price = stock_data["price"]
                holding_value = market_price * asset.quantity
                total_value += holding_value
            except Exception:
                market_price = None
                holding_value = None

            purchase_value = asset.purchase_price * asset.quantity
            profit_loss = None
            return_percent = None

            if holding_value is not None:
                profit_loss = holding_value - purchase_value
                if purchase_value > 0:
                    return_percent = (profit_loss / purchase_value) * 100

            valued_assets.append({
                "symbol": asset.symbol,
                "name": asset.name,
                "quantity": asset.quantity,
                "market_price": market_price,
                "holding_value": holding_value,
                "purchase_price": asset.purchase_price,
                "purchase_value": purchase_value,
                "profit_loss": profit_loss,
                "return_percent": return_percent
            })

        return valued_assets, total_value

    def get_total_assets(self):
        return len(self._assets)

    def get_assets(self):
        return self._assets
