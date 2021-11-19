import yfinance


data = yfinance.download(["BTC-USD"], start="2021-11-11", end="2021-11-18", interval="1h")
data.to_csv("data.csv")