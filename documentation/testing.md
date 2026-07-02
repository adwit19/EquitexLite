# Equitex Lite Testing

| Test ID | Feature | Test Input | Expected Result | Actual Result | Pass/Fail |
|----------|----------|------------|-----------------|---------------|-----------|
| T1 | Search Stock | AAPL | Apple stock displayed | | |
| T2 | Search Stock | INVALID123 | Error message | | |
| T3 | Add Stock | AAPL, Qty 10 | Stock added | | |
| T4 | Duplicate Stock | AAPL again | Quantity updated | | |
| T5 | Remove Stock | Remove AAPL | Stock removed | | |
| T6 | Save Portfolio | Save and reopen | Portfolio restored | | |
| T7 | Portfolio Value | Multiple stocks | Correct total value | | |
| T8 | Purchase Price | Enter purchase price | Profit/Loss calculated | | |
| T9 | Price History | AAPL | Chart displayed | | |
| T10 | Allocation Chart | Portfolio | Pie chart displayed | | |
| T11 | Theme Toggle | Click switch | Theme changes | | |

py run_gui.py

