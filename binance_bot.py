
import smtplib
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import datetime as dt
from time import sleep
from email.message import EmailMessage

client = Client(api_key, api_secret)

currencies=[]
purchased_currencies=[]

purchase_amount = 10
minimum_account_amount = 20

prev_update = dt.datetime.now()

def send_email(title, body):
    sender_address = from_adress
    receiver_address = to_adress
    account_password = password
    smtp_server = smtplib.SMTP_SSL(smtp_server, 465)
    smtp_server.login(sender_address, account_password)
    message = f"Subject: {title}\n\n{body}"
    smtp_server.sendmail(sender_address, receiver_address, message)
    smtp_server.close()


def get_available_currency(symbol):
    available_currency = float(client.get_asset_balance(asset=symbol)['free'])
    print(round(available_currency,2), symbol+' available')
    return available_currency

def purchase_description(symbol, value, order):
    price = float(client.get_symbol_ticker(symbol=symbol)['price'])

    l1 = 'Purchased ' + str(round(value/price,4)) + symbol + ' for ' + str(value)
    l2 = 'Order description: ' + str(order)


    return l1+'\n'+l2

def buy(symbol, value):
    order = client.create_order(
        symbol=symbol,
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quoteOrderQty=value)
    print('Order placed for '+symbol)
    purchased_currencies.append(symbol)

    sleep(10)

    send_email('New currency purchased!', purchase_description(symbol, value, order))


def place_sell_order(symbol, amount, price):
    order = client.create_order(
        symbol=symbol,
        side=Client.SIDE_SELL,
        type=Client.ORDER_TYPE_LIMIT,
        quantity=amount,
        price=str(price))
    print('Sell order placed for '+symbol)


def invest_in_currency(currency):
    available_busd = get_available_currency('BUSD')
    if available_busd >= minimum_account_amount + purchase_amount:
        buy(currency['symbol'], purchase_amount)
        purchased_currencies.append(currency['symbol'])
        print('Purchased. Sleeping for 60s before placing sell order.')

        sleep(60)

        print('Placing sell order at 3x price')
        updated_price = float(client.get_symbol_ticker(symbol=currency['symbol'])['price'])
        amount_possessed = get_available_currency(currency['symbol'])
        sell_price = 3*updated_price
        place_sell_order(currency[symbol], amount_possessed, sell_price)

    else: print('Not enough funds to make purchase.')


res = client.get_exchange_info()
print(client.response.headers)

for currency in client.get_all_tickers():
    if currency['symbol'] not in currencies and 'BUSD' in currency['symbol']:
        currencies.append(currency['symbol'])
print('Initially found '+str(len(currencies))+' currencies.')




while True:
    found_new=False
    for currency in client.get_all_tickers():
        if currency['symbol'] not in currencies and 'BUSD' in currency['symbol']:
            currencies.append(currency['symbol'])
            print(dt.datetime.now(), 'Found new currency!')
            print(currency['symbol'], currency['price'])
            print('Purchasing...')
            invest_in_currency(currency)
            found_new=True
    if found_new==False: print(dt.datetime.now(), 'No new currency found.')

    sleep(60)
    if (dt.datetime.now()-prev_update).seconds>3600:
        body='Email sent at: '+str(dt.datetime.now())+'\nCurrent currencies count: '+str(len(currencies))+'\nHas invested in: '+str(purchased_currencies)+'\n\nAll available currencies: '+str(currencies)
        send_email('Program running...', body)
        prev_update = dt.datetime.now()




















