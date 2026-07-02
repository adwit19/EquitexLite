from tkinter import ttk

import customtkinter
import matplotlib.pyplot as plt
import yfinance as yf

from models.stock import Stock
from services.api_manager import APIManager
from services.file_manager import FileManager

try:
    from CTkMessagebox import CTkMessagebox
except ImportError:
    CTkMessagebox = None


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class EquitexApp(customtkinter.CTk):
    """Main CustomTkinter application for Equitex Lite."""

    def __init__(self):
        """Initialize the Equitex Lite application window."""
        super().__init__()

        self.title("Equitex Lite")
        self.geometry("1000x700")
        self.current_stock = None
        self.portfolio = FileManager.load_portfolio()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.create_search_section()
        self.create_stock_information_section()

        self.portfolio_table_frame = customtkinter.CTkFrame(self)
        self.portfolio_table_frame.grid(
            row=2,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="nsew"
        )
        self.portfolio_table_frame.grid_columnconfigure(0, weight=1)
        self.portfolio_table_frame.grid_rowconfigure(1, weight=1)

        self.portfolio_title_label = customtkinter.CTkLabel(
            self.portfolio_table_frame,
            text="Portfolio",
            anchor="w",
            font=customtkinter.CTkFont(size=16, weight="bold")
        )
        self.portfolio_title_label.grid(
            row=0,
            column=0,
            padx=15,
            pady=(15, 5),
            sticky="w"
        )

        self.portfolio_table = ttk.Treeview(
            self.portfolio_table_frame,
            columns=(
                "Ticker",
                "Company",
                "Quantity",
                "Purchase Price",
                "Current Price",
                "Holding Value",
                "Profit/Loss",
                "Return %"
            ),
            show="headings"
        )
        self.portfolio_table.grid(
            row=1,
            column=0,
            padx=(15, 0),
            pady=15,
            sticky="nsew"
        )

        self.portfolio_table.heading("Ticker", text="Ticker")
        self.portfolio_table.heading("Company", text="Company")
        self.portfolio_table.heading("Quantity", text="Quantity")
        self.portfolio_table.heading("Purchase Price", text="Purchase Price")
        self.portfolio_table.heading("Current Price", text="Current Price")
        self.portfolio_table.heading("Holding Value", text="Holding Value")
        self.portfolio_table.heading("Profit/Loss", text="Profit/Loss")
        self.portfolio_table.heading("Return %", text="Return %")

        self.portfolio_table.column("Ticker", width=100, anchor="center")
        self.portfolio_table.column("Company", width=250)
        self.portfolio_table.column("Quantity", width=100, anchor="center")
        self.portfolio_table.column("Purchase Price", width=120, anchor="e")
        self.portfolio_table.column("Current Price", width=120, anchor="e")
        self.portfolio_table.column("Holding Value", width=120, anchor="e")
        self.portfolio_table.column("Profit/Loss", width=120, anchor="e")
        self.portfolio_table.column("Return %", width=100, anchor="e")

        self.portfolio_scrollbar = ttk.Scrollbar(
            self.portfolio_table_frame,
            orient="vertical",
            command=self.portfolio_table.yview
        )
        self.portfolio_scrollbar.grid(
            row=1,
            column=1,
            padx=(0, 15),
            pady=15,
            sticky="ns"
        )
        self.portfolio_table.configure(
            yscrollcommand=self.portfolio_scrollbar.set
        )

        self.analytics_frame = customtkinter.CTkFrame(self.portfolio_table_frame)
        self.analytics_frame.grid(
            row=2,
            column=0,
            columnspan=2,
            padx=15,
            pady=(0, 15),
            sticky="ew"
        )
        self.analytics_frame.grid_columnconfigure(0, weight=1)
        self.analytics_frame.grid_columnconfigure(1, weight=1)

        self.analytics_title_label = customtkinter.CTkLabel(
            self.analytics_frame,
            text="Portfolio Analytics",
            anchor="w",
            font=customtkinter.CTkFont(size=14, weight="bold")
        )
        self.analytics_title_label.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=(10, 10),
            sticky="w"
        )

        self.total_holdings_label = customtkinter.CTkLabel(
            self.analytics_frame,
            text="Total Holdings: 0",
            anchor="w"
        )
        self.total_holdings_label.grid(
            row=1,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.total_value_analytics_label = customtkinter.CTkLabel(
            self.analytics_frame,
            text="Portfolio Value: $0.00",
            anchor="w"
        )
        self.total_value_analytics_label.grid(
            row=1,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.largest_holding_label = customtkinter.CTkLabel(
            self.analytics_frame,
            text="Largest Holding: -",
            anchor="w"
        )
        self.largest_holding_label.grid(
            row=2,
            column=0,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.largest_value_label = customtkinter.CTkLabel(
            self.analytics_frame,
            text="Largest Holding Value: -",
            anchor="w"
        )
        self.largest_value_label.grid(
            row=2,
            column=1,
            padx=10,
            pady=5,
            sticky="w"
        )

        self.average_holding_label = customtkinter.CTkLabel(
            self.analytics_frame,
            text="Average Holding Value: -",
            anchor="w"
        )
        self.average_holding_label.grid(
            row=3,
            column=0,
            columnspan=2,
            padx=10,
            pady=(5, 10),
            sticky="w"
        )

        self.bottom_toolbar = customtkinter.CTkFrame(self)
        self.bottom_toolbar.grid(
            row=3,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="ew"
        )
        self.bottom_toolbar.grid_columnconfigure(0, weight=1)

        self.total_value_label = customtkinter.CTkLabel(
            self.bottom_toolbar,
            text="Total Portfolio Value: $0.00"
        )
        self.total_value_label.grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="w"
        )

        self.save_button = customtkinter.CTkButton(
            self.bottom_toolbar,
            text="Save"
        )
        self.save_button.grid(row=0, column=1, padx=(10, 5), pady=15)

        self.remove_button = customtkinter.CTkButton(
            self.bottom_toolbar,
            text="Remove Selected Stock",
            command=self.remove_selected_stock
        )
        self.remove_button.grid(row=0, column=2, padx=5, pady=15)

        self.show_chart_button = customtkinter.CTkButton(
            self.bottom_toolbar,
            text="Show Price History",
            command=self.show_price_history
        )
        self.show_chart_button.grid(row=0, column=3, padx=5, pady=15)

        self.allocation_button = customtkinter.CTkButton(
            self.bottom_toolbar,
            text="Portfolio Allocation",
            command=self.show_portfolio_allocation
        )
        self.allocation_button.grid(row=0, column=4, padx=(5, 15), pady=15)

        self.status_label = customtkinter.CTkLabel(
            self,
            text="Ready",
            anchor="w"
        )
        self.status_label.grid(
            row=4,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="ew"
        )

        self.refresh_portfolio_table()

    def create_search_section(self):
        """Create the stock search controls at the top of the window."""
        self.search_frame = customtkinter.CTkFrame(self)
        self.search_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        self.search_frame.grid_columnconfigure(1, weight=1)

        self.search_label = customtkinter.CTkLabel(
            self.search_frame,
            text="Search Stock"
        )
        self.search_label.grid(row=0, column=0, padx=(15, 10), pady=15)

        self.search_entry = customtkinter.CTkEntry(
            self.search_frame,
            placeholder_text="Enter ticker (e.g. AAPL, MSFT, NVDA, TSLA...)"
        )
        self.search_entry.grid(row=0, column=1, padx=10, pady=15, sticky="ew")

        self.search_button = customtkinter.CTkButton(
            self.search_frame,
            text="Search",
            command=self.search_stock
        )
        self.search_button.grid(row=0, column=2, padx=(10, 15), pady=15)

        self.appearance_mode_var = customtkinter.StringVar(value="Light")
        self.appearance_mode_switch = customtkinter.CTkSwitch(
            self.search_frame,
            text="Dark Mode",
            command=self.toggle_appearance_mode,
            variable=self.appearance_mode_var,
            onvalue="Dark",
            offvalue="Light"
        )
        self.appearance_mode_switch.grid(
            row=0,
            column=3,
            padx=(0, 15),
            pady=15,
            sticky="e"
        )

    def create_stock_information_section(self):
        """Create the stock information controls below search."""
        self.stock_info_frame = customtkinter.CTkFrame(self)
        self.stock_info_frame.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 20),
            sticky="ew"
        )
        self.stock_info_frame.grid_columnconfigure(0, weight=1)

        self.symbol_label = customtkinter.CTkLabel(
            self.stock_info_frame,
            text="Symbol: -",
            anchor="w"
        )
        self.symbol_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(18, 6),
            sticky="ew"
        )

        self.company_label = customtkinter.CTkLabel(
            self.stock_info_frame,
            text="Company: -",
            anchor="w"
        )
        self.company_label.grid(
            row=1,
            column=0,
            padx=20,
            pady=6,
            sticky="ew"
        )

        self.price_label = customtkinter.CTkLabel(
            self.stock_info_frame,
            text="Current Price: -",
            anchor="w"
        )
        self.price_label.grid(
            row=2,
            column=0,
            padx=20,
            pady=(6, 18),
            sticky="ew"
        )

        self.add_button = customtkinter.CTkButton(
            self.stock_info_frame,
            text="Add to Portfolio",
            command=self.add_current_stock
        )
        self.add_button.grid(
            row=0,
            column=1,
            rowspan=3,
            padx=(10, 20),
            pady=20
        )

    def search_stock(self):
        """Look up the ticker entered in the search box."""
        symbol = self.search_entry.get().strip().upper()

        if symbol == "":
            self.reset_stock_information()
            self.show_search_error("Please enter a ticker symbol.")
            return

        try:
            self.current_stock = APIManager.get_stock_data(symbol)
            self.update_stock_information()
            print(self.current_stock)
        except Exception:
            self.current_stock = None
            self.reset_stock_information()
            self.show_search_error("Stock lookup failed.")

    def show_search_error(self, message):
        """Show a search error using CTkMessagebox when available."""
        if CTkMessagebox is not None:
            CTkMessagebox(title="Search Error", message=message)
        else:
            print(message)

    def toggle_appearance_mode(self):
        """Toggle between light and dark appearance modes."""
        mode = self.appearance_mode_var.get()
        customtkinter.set_appearance_mode(mode)

    def update_stock_information(self):
        """Update stock information labels after a successful search."""
        symbol = self.current_stock["symbol"]
        company = self.current_stock["name"]
        price = self.current_stock["price"]

        self.symbol_label.configure(text=f"Symbol: {symbol}")
        self.company_label.configure(text=f"Company: {company}")
        self.price_label.configure(text=f"Current Price: ${price:.2f}")

    def reset_stock_information(self):
        """Reset stock information labels to their placeholder values."""
        self.symbol_label.configure(text="Symbol: -")
        self.company_label.configure(text="Company: -")
        self.price_label.configure(text="Current Price: -")

    def add_current_stock(self):
        """Handle the add-to-portfolio button press."""
        if self.current_stock is None:
            self.show_search_error("Search for a stock before adding it.")
            return

        quantity = self.ask_quantity()

        if quantity is None:
            return

        symbol = self.current_stock["symbol"]
        company = self.current_stock["name"]

        purchase_price = self.ask_purchase_price()

        if purchase_price is None:
            return

        if self.stock_exists(symbol):
            self.portfolio.update_quantity(symbol, quantity, purchase_price)
        else:
            stock = Stock(symbol, company, quantity, purchase_price)
            self.portfolio.add_asset(stock)

        FileManager.save_portfolio(self.portfolio)
        self.refresh_portfolio_table()
        self.show_success_message(f"{symbol} added to portfolio.")

    def ask_quantity(self):
        """Ask the user for a positive share quantity."""
        dialog = customtkinter.CTkInputDialog(
            text="How many shares do you own?",
            title="Add to Portfolio"
        )
        quantity_input = dialog.get_input()

        return self.validate_quantity(quantity_input)

    def ask_purchase_price(self):
        """Ask the user for a positive purchase price per share."""
        dialog = customtkinter.CTkInputDialog(
            text="What was the purchase price per share?",
            title="Purchase Price"
        )
        purchase_price_input = dialog.get_input()

        return self.validate_purchase_price(purchase_price_input)

    def validate_quantity(self, quantity_input):
        """Validate and return a positive numeric quantity."""
        if quantity_input is None:
            return None

        quantity_input = quantity_input.strip()

        if quantity_input == "":
            self.show_search_error("Quantity cannot be empty.")
            return None

        try:
            quantity = float(quantity_input)
        except ValueError:
            self.show_search_error("Please enter a valid number.")
            return None

        if quantity <= 0:
            self.show_search_error("Quantity must be greater than 0.")
            return None

        return quantity

    def validate_purchase_price(self, purchase_price_input):
        """Validate and return a positive purchase price."""
        if purchase_price_input is None:
            return None

        purchase_price_input = purchase_price_input.strip()

        if purchase_price_input == "":
            self.show_search_error("Purchase price cannot be empty.")
            return None

        try:
            purchase_price = float(purchase_price_input)
        except ValueError:
            self.show_search_error("Please enter a valid purchase price.")
            return None

        if purchase_price <= 0:
            self.show_search_error("Purchase price must be greater than 0.")
            return None

        return purchase_price

    def stock_exists(self, symbol):
        """Return True when the symbol is already in the portfolio."""
        for asset in self.portfolio.get_assets():
            if asset.symbol == symbol:
                return True

        return False

    def remove_selected_stock(self):
        """Remove the selected stock from the portfolio table."""
        selected_item = self.portfolio_table.selection()

        if not selected_item:
            self.show_search_error("Please select a stock to remove.")
            return

        ticker = self.portfolio_table.item(selected_item, "values")[0]

        if self.portfolio.remove_asset(ticker):
            FileManager.save_portfolio(self.portfolio)
            self.refresh_portfolio_table()
            self.show_success_message(f"{ticker} removed from portfolio.")
        else:
            self.show_search_error("Failed to remove the selected stock.")

    def show_price_history(self):
        """Show one year of price history for the selected portfolio stock."""
        selected_item = self.portfolio_table.selection()

        if not selected_item:
            self.show_search_error("Please select a stock before showing price history.")
            return

        ticker = self.portfolio_table.item(selected_item, "values")[0]

        try:
            stock = yf.Ticker(ticker)
            history = stock.history(period="1y")

            if history.empty:
                self.show_search_error("No historical data available for the selected stock.")
                return

            dates = history.index
            prices = history["Close"].fillna(method="ffill").fillna(method="bfill")

            plt.figure()
            plt.plot(dates, prices)
            plt.title(f"{ticker} Price History")
            plt.xlabel("Date")
            plt.ylabel("Price ($)")
            plt.grid(True)
            plt.tight_layout()
            plt.show()
        except Exception:
            self.show_search_error("Failed to retrieve price history.")

    def show_portfolio_allocation(self):
        """Display a pie chart of portfolio allocation by holding value."""
        valued_assets, total_value = self.portfolio.calculate_total_value()

        if total_value == 0 or not valued_assets:
            self.show_search_error("Portfolio is empty or has no allocatable holdings.")
            return

        labels = []
        sizes = []

        for asset in valued_assets:
            if asset["holding_value"] is None:
                continue

            labels.append(asset["name"])
            sizes.append(asset["holding_value"])

        if not sizes or sum(sizes) == 0:
            self.show_search_error("Portfolio is empty or has no allocatable holdings.")
            return

        percentages = [100 * value / total_value for value in sizes]
        label_texts = [f"{label} ({percentage:.1f}%)" for label, percentage in zip(labels, percentages)]

        plt.figure()
        plt.pie(sizes, labels=label_texts, autopct=None)
        plt.title("Portfolio Allocation")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

    def refresh_portfolio_table(self):
        """Refresh portfolio table contents and update the total value label."""
        if not hasattr(self, "portfolio_table"):
            return

        for row_id in self.portfolio_table.get_children():
            self.portfolio_table.delete(row_id)

        valued_assets, total_value = self.portfolio.calculate_total_value()

        for asset in valued_assets:
            if asset["market_price"] is None:
                price = "Unavailable"
                value = "Unavailable"
                profit_loss = "Unavailable"
                return_percent = "Unavailable"
            else:
                price = f"${asset['market_price']:.2f}"
                value = f"${asset['holding_value']:.2f}"

                if asset["profit_loss"] is None:
                    profit_loss = "Unavailable"
                else:
                    profit_loss_value = asset["profit_loss"]
                    sign = "+" if profit_loss_value >= 0 else "-"
                    profit_loss = f"{sign}${abs(profit_loss_value):.2f}"

                if asset["return_percent"] is None:
                    return_percent = "Unavailable"
                else:
                    return_percent_value = asset["return_percent"]
                    sign = "+" if return_percent_value >= 0 else "-"
                    return_percent = f"{sign}{abs(return_percent_value):.1f}%"

            purchase_price = f"${asset['purchase_price']:.2f}"

            self.portfolio_table.insert(
                "",
                "end",
                values=(
                    asset["symbol"],
                    asset["name"],
                    f"{asset['quantity']:g}",
                    purchase_price,
                    price,
                    value,
                    profit_loss,
                    return_percent
                )
            )

        self.total_value_label.configure(
            text=f"Total Portfolio Value: ${total_value:.2f}"
        )
        self.refresh_analytics(valued_assets, total_value)

    def refresh_analytics(self, valued_assets=None, total_value=None):
        """Refresh portfolio analytics using the current portfolio values."""
        if valued_assets is None or total_value is None:
            valued_assets, total_value = self.portfolio.calculate_total_value()

        total_holdings = len(valued_assets)

        if total_holdings == 0 or total_value == 0:
            self.total_holdings_label.configure(text="Total Holdings: 0")
            self.total_value_analytics_label.configure(text="Portfolio Value: $0.00")
            self.largest_holding_label.configure(text="Largest Holding: -")
            self.largest_value_label.configure(text="Largest Holding Value: -")
            self.average_holding_label.configure(text="Average Holding Value: -")
            return

        valid_assets = [asset for asset in valued_assets if asset["holding_value"] is not None]

        if valid_assets:
            largest_asset = max(valid_assets, key=lambda asset: asset["holding_value"])
            largest_name = largest_asset["name"]
            largest_value = largest_asset["holding_value"]
        else:
            largest_name = "-"
            largest_value = None

        average_value = total_value / total_holdings if total_holdings else 0

        self.total_holdings_label.configure(text=f"Total Holdings: {total_holdings}")
        self.total_value_analytics_label.configure(
            text=f"Portfolio Value: ${total_value:.2f}"
        )
        self.largest_holding_label.configure(
            text=f"Largest Holding: {largest_name}"
        )
        self.largest_value_label.configure(
            text=f"Largest Holding Value: ${largest_value:.2f}"
            if largest_value is not None else "Largest Holding Value: -"
        )
        self.average_holding_label.configure(
            text=f"Average Holding Value: ${average_value:.2f}"
        )

    def show_success_message(self, message):
        """Show a success message after a portfolio action."""
        self.status_label.configure(text=message)

        if CTkMessagebox is not None:
            CTkMessagebox(title="Success", message=message)
        else:
            print(message)


if __name__ == "__main__":
    app = EquitexApp()
    app.mainloop()
