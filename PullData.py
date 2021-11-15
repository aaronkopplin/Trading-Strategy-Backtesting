import yfinance


data = yfinance.download(["BTC-USD"], start="2021-09-25", end="2021-11-13", interval="15m")
data.to_csv("data.csv")