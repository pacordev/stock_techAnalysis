# %%
"""
Importing libraries used
yfinance = to get the stock data from Yahoo
pandas   = to manage the dataframes with the stock data
matplotlib = to create the dashboards for visualization 
"""
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use("Agg")   # we need to use non-interactive backend (no GUI window) to avoid displaying the plot
import matplotlib.pyplot as pltstk
from datetime import datetime, timedelta

# %%
"""
Let's create some variables to use in our script
"""
initial_date = '2025-10-01'
hoy = datetime.now().strftime("%Y%m%d")
ayer = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
stock = 'BNS'

# %%
# initially we will download info from the stock, from the last 3 months. Eventually we will split the script to download the info into a database and read from there
"""
initially we will download info for 1 stock, from the last 3 months.
options used:
    ticker: the stock ticker from which we want to download info
    start:  start date of the period of information we want to download, inclusive
    end:    end date of the period of information we want to download, exclusive
    auto_adjust:    To adjust the Open-high-low-close columns. if False, add a column for Adjusted close value
    rounding:   To round values to 2 decimal places
    multi_level_index:  To manage column names as multilevel index. Set to talse to get a single level columns name
"""
datos_stock = yf.download(stock, start=initial_date, end=ayer, auto_adjust=False, rounding=True, multi_level_index=False)

# %%
"""
we calculate MACD indicators and signal line.
we will use a simple Open-high-low-close dashboard and focus only on closing

"""
datos_stock['EMA12'] = datos_stock['Close'].ewm(span=12, adjust=False).mean()
datos_stock['EMA26'] = datos_stock['Close'].ewm(span=26, adjust=False).mean()
datos_stock['MACD'] = datos_stock['EMA12'] - datos_stock['EMA26']
datos_stock['Signal'] = datos_stock['MACD'].ewm(span=9, adjust=False).mean()

# %%
"""
We will plot an initial graph for our MACD
    - MACD line shows momentum shifts.
    - Signal line helps identify buy/sell signals.
    - When MACD crosses above the signal line → potential buy.
    - When MACD crosses below → potential sell.
"""
#pltstk.figure(figsize=(12,6))
pltstk.figure(figsize=(10,5))
pltstk.plot(datos_stock.index, datos_stock['MACD'], label='MACD - cross above signal, buy', color='blue')              # to show momentum shift
pltstk.plot(datos_stock.index, datos_stock['Signal'], label='Signal Line', color='red')      # to show buy/sel signals
pltstk.legend(loc='upper left')
pltstk.title(f"MACD Indicator for {stock}")

# %%
# now, let's save the plot as an image. Optionally, we show the plot.
output_path = f"./{stock}_dash_{hoy}.png"
pltstk.savefig(output_path, dpi=300, bbox_inches='tight')
pltstk.close()

print(f"Simple dashboard-style for {stock} with MACD, saved as {stock}_dashboard.png")