# Binance-Bot

Simple Python Bot that invests immediatly in newly created cryptocurrencies.

 - Checks every 60 seconds for new currencies (that can be purchased using BUSD)
 - If a new one is found, the bot will invest 10$ using the Binance API (if account balance is above minimum amount) and send you an email notifying you of the purchase
 - The bot will also place a sell order at 3x initial price

The bot sends you an email every hour (time interval may easily be modified) to inform you that the program is still running (includes timestamp), as well as give you an update of the available currencies + purchased currencies

These values can be customized as one wishes to allow for higher/lower risk, or to access other markets.
Feel free to use it yourself (at your own risk) and suggest improvements :)
