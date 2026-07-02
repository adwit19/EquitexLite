import json
from pathlib import Path

from models.portfolio import Portfolio
from models.stock import Stock


class FileManager:
    """
    Handles saving and loading portfolio data from a JSON file.
    """

    FILE_PATH = Path("data/portfolio.json")

    @staticmethod
    def save_portfolio(portfolio):
        if not isinstance(portfolio, Portfolio):
            raise TypeError("save_portfolio expects a Portfolio object.")

        assets = []

        for asset in portfolio.get_assets():
            assets.append({
                "symbol": asset.symbol,
                "name": asset.name,
                "quantity": asset.quantity,
                "purchase_price": getattr(asset, "purchase_price", 0.0)
            })

        FileManager.FILE_PATH.parent.mkdir(parents=True, exist_ok=True)

        with open(FileManager.FILE_PATH, "w") as file:
            json.dump(assets, file, indent=4)

    @staticmethod
    def load_portfolio():
        portfolio = Portfolio()

        if not FileManager.FILE_PATH.exists():
            return portfolio

        with open(FileManager.FILE_PATH, "r") as file:
            assets = json.load(file)

        for asset in assets:
            stock = Stock(
                asset["symbol"],
                asset["name"],
                asset.get("quantity", 1),
                asset.get("purchase_price", 0.0)
            )
            portfolio.add_asset(stock)

        return portfolio
