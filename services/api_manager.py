import yfinance as yf


class APIManager:

    @staticmethod
    def get_stock_data(symbol):

        ticker = yf.Ticker(symbol)

        history = ticker.history(period="1d")

        if history.empty:
            raise Exception("Ticker not found")

        price = round(history["Close"].iloc[-1], 2)

        return {
            "symbol": symbol.upper(),
            "name": symbol.upper(),
            "price": price
        }