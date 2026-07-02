from services.api_manager import APIManager
from services.file_manager import FileManager
from models.stock import Stock


def display_menu():
    print("\nEquitex Lite")
    print("1. Search Stock")
    print("2. Add Stock")
    print("3. View Portfolio")
    print("4. Remove Stock")
    print("5. Save Portfolio")
    print("6. Exit")


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

    symbol = stock_data["symbol"]

    for asset in portfolio.get_assets():
        if asset.symbol == symbol:
            choice = input("This stock already exists. Add to the existing quantity? (Y/N) ").strip().upper()

            if choice != "Y":
                print("Operation cancelled.")
                return

            quantity = ask_stock_quantity()
            portfolio.update_quantity(symbol, quantity)
            print(f"{symbol} quantity updated.")
            return

    quantity = ask_stock_quantity()
    stock = Stock(symbol, stock_data["name"], quantity)
    portfolio.add_asset(stock)
    print(f"{stock.symbol} added to portfolio.")


def ask_stock_quantity():
    while True:
        quantity_input = input("How many shares do you own? ").strip()

        try:
            quantity = float(quantity_input)
        except ValueError:
            print("Please enter a valid number of shares.")
            continue

        if quantity <= 0:
            print("Quantity must be greater than 0.")
            continue

        return quantity


def remove_stock(portfolio):
    symbol = input("Enter stock symbol to remove: ").strip()

    if symbol == "":
        print("Please enter a stock symbol.")
        return

    if portfolio.remove_asset(symbol):
        print(f"{symbol.upper()} removed from portfolio.")
    else:
        print(f"{symbol.upper()} was not found in your portfolio.")


def view_portfolio(portfolio):
    assets = portfolio.get_assets()

    if len(assets) == 0:
        print("Your portfolio is empty.")
        return

    valued_assets, total_value = portfolio.calculate_total_value()

    print("\nPortfolio")
    print(f"{'Ticker':<8} {'Company':<20} {'Qty':<6} {'Price':<12} {'Value':<12}")
    print("-" * 60)

    for asset in valued_assets:
        if asset["market_price"] is None:
            price = "Unavailable"
            value = "Unavailable"
        else:
            price = f"${asset['market_price']:.2f}"
            value = f"${asset['holding_value']:.2f}"

        print(
            f"{asset['symbol']:<8} "
            f"{asset['name']:<20} "
            f"{asset['quantity']:<6g} "
            f"{price:<12} "
            f"{value:<12}"
        )

    print("-" * 60)
    print(f"Total Portfolio Value: ${total_value:.2f}")


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
            remove_stock(portfolio)
        elif choice == "5":
            FileManager.save_portfolio(portfolio)
            print("Portfolio saved.")
        elif choice == "6":
            FileManager.save_portfolio(portfolio)
            print("Portfolio saved.")
            print("Goodbye.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()

    
