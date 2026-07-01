from services.api_manager import APIManager
from services.file_manager import FileManager
from models.stock import Stock


def display_menu():
    print("\nEquitex Lite")
    print("1. Search Stock")
    print("2. Add Stock")
    print("3. View Portfolio")
    print("4. Save Portfolio")
    print("5. Exit")


def search_stock():
    symbol = input("Enter stock symbol: ").strip()

    if symbol == "":
        print("Please enter a stock symbol.")
        return None

    try:
        stock_data = APIManager.get_stock_data(symbol)
        print(f"Symbol: {stock_data['symbol']}")
        print(f"Name: {stock_data['name']}")
        print(f"Price: {stock_data['price']}")
        return stock_data
    except Exception as error:
        print(f"Stock lookup failed: {error}")
        return None


def add_stock(portfolio):
    stock_data = search_stock()

    if stock_data is None:
        return

    stock = Stock(stock_data["symbol"], stock_data["name"])
    portfolio.add_asset(stock)
    print(f"{stock.symbol} added to portfolio.")


def view_portfolio(portfolio):
    assets = portfolio.display_assets()

    if len(assets) == 0:
        print("Your portfolio is empty.")
        return

    print("\nPortfolio")

    for asset in assets:
        print(asset)

    print(f"Total assets: {portfolio.get_total_assets()}")


def main():
    portfolio = FileManager.load_portfolio()

    while True:
        display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            search_stock()
        elif choice == "2":
            add_stock(portfolio)
        elif choice == "3":
            view_portfolio(portfolio)
        elif choice == "4":
            FileManager.save_portfolio(portfolio)
            print("Portfolio saved.")
        elif choice == "5":
            FileManager.save_portfolio(portfolio)
            print("Portfolio saved.")
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()

    
