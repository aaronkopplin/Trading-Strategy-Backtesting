import yfinance


data = yfinance.download(["BTC-USD"], start="2021-10-15", end="2021-11-13", interval="1d")
data.to_csv("data.csv")