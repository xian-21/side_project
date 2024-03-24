# from binance.spot import Spot
from binance.client import Client
import requests
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pykrakenapi import KrakenAPI
import urllib.parse
import hashlib
import hmac
import base64
from max.client import Client as m_client
import traceback

'''
程式流程:
    先幣安、max交易所的錢包餘額，並且將餘額儲存成資料變數，接著使用api取得指定交易對在幣安以及max交易所的
    價格、交易數量、買賣方向，並且計算指定交易對在兩家交易所的價差是否大於交易手續費，如果大於交易手續費就有
    套利空間可以獲利，接著如果沒有套利空間就繼續重複剛剛的步驟直到有套利空間，如果有套利空間就會馬上在兩家交易所
    同時下買賣單，一買一賣來進行套利，最後取得錢包餘額計算實際獲利，並且記錄在net_profit裡面，接著繼續剛剛的步驟
    直到找到下一次套利空間
'''



def binance_sell_buy(ordertype,symbol,side, price, quantity ):
    # Binance API endpoint
    url = 'https://api.binance.com/api/v3/order'
    # API endpoint parameters
    params = {
        'symbol': symbol,
        'side': side,
        'type': ordertype,
        'timeInForce': 'GTC',
        'quantity': quantity,
        'price': price,
        'timestamp': int(time.time() * 1000),
    }
    api_secret = ''
    query_string = '&'.join([f"{key}={params[key]}" for key in params])
    signature = hmac.new(api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    params['signature'] = signature
    headers = {'X-MBX-APIKEY': ''}
    response = requests.post(url, params=params, headers=headers)
    print(f"binance {side}\n{response.json()}")

def binance_check_balance():
    # 幣安查詢賬戶信息
    account_info = client.get_account()
    # 打印指定幣種的餘額
    for balance in account_info['balances']:
        asset = balance['asset']
        free = float(balance['free'])  # 可用餘額
        if asset in binance_balance.keys():
            binance_balance[asset] = free

def binance_get_price():
    global binance_bid_price, binance_bid_quantity, binance_ask_price, binance_ask_quantity,binance_data_dict
    binance_data_dict = {item['symbol']: item for item in tickers}
    binance_bid_price = float(binance_data_dict[i]['bidPrice'])  # 最高的買單價
    binance_bid_quantity = float(binance_data_dict[i]['bidQty'])  # 最高買單的數量
    binance_ask_price = float(binance_data_dict[i]['askPrice'])  # 最低的賣單價
    binance_ask_quantity = float(binance_data_dict[i]['askQty'])  # 最低賣單的數量

def smtp(mail):
    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "套利統計"  #郵件標題
    content["from"] = "a8979401551@gmail.com"  #寄件者
    content["to"] = "C108157126@nkust.edu.tw" #收件者
    
    # content.attach(MIMEImage(Path(screenshot_name).read_bytes()))  #郵件圖片
    content.attach(MIMEText(mail))  #郵件內容

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login("a8979401551@gmail.com", "")  # 登入寄件者gmail(google雙重驗證應用程式密碼)
            smtp.send_message(content)  # 寄送郵件
            print("send email Complete!")
        except Exception as e:
            print("Error message: ", e)

def binance_history_order():#取得最近一筆市價交易價格
    resp = client.get_my_trades(symbol=i,limit=2)
    if resp[0]['isBuyer'] == True:
        buy_price[buy_exchange] = float(resp[0]['price'])
    elif resp[0]['isMaker'] == True:
        sell_price[sell_exchange] = float(resp[0]['price'])
        
def kraken_get_price():
    global kraken_b, kraken_b_quantity, kraken_a, kraken_a_quantity
    #kraken 取得報價
    kraken_data = kraken_price_resp.json()
    if i == 'DOGEUSDT':
        kraken_b = float(kraken_data['result']['XDGUSDT']['b'][0]) # 最高的買單價
        kraken_b_quantity = float(kraken_data['result']['XDGUSDT']['b'][1])# 最高買單的數量
        kraken_a = float(kraken_data['result']['XDGUSDT']['a'][0]) # 最低的賣單價
        kraken_a_quantity = float(kraken_data['result']['XDGUSDT']['a'][1])# 最低賣單的數量
    else:# 解析 JSON 響應
        kraken_b = float(kraken_data['result'][i]['b'][0]) # 最高的買單價
        kraken_b_quantity = float(kraken_data['result'][i]['b'][1])# 最高買單的數量
        kraken_a = float(kraken_data['result'][i]['a'][0]) # 最低的賣單價
        kraken_a_quantity = float(kraken_data['result'][i]['a'][1])# 最低賣單的數量

def max_get_price():
    global max_bid_price, max_bid_quantity, max_ask_price, max_ask_quantity
    #max取得報價
    max_data = response.json()
    max_bid_price = float(max_data[i.lower()]['buy'])  # 最高的買單價
    max_bid_quantity = float(max_data[i.lower()]['buy_vol'])  # 最高買單的數量
    max_ask_price = float(max_data[i.lower()]['sell']) # 最低的賣單價
    max_ask_quantity = float(max_data[i.lower()]['sell_vol'])   # 最低賣單的數量

def max_check_balance():
    max_balance_data = max_client.get_private_account_balances()
    for i in max_balance_data:
        if i['currency'] in ['link','xrp','ada','matic','sol','dot','ltc','doge','usdt','twd']:
            max_balance[i['currency'].upper()] = float(i['balance'])
            
def max_sell_buy(pair, side, price, volume):
    response = max_client.set_private_create_order(pair, side, volume, price)
    print(f"max {side}\n{response}")
    

def buy_sell():
    global trade_quantity
    if sell_exchange == 'binance' and buy_exchange == 'max':#幣安賣 max買
        trade_quantity = min(max_balance[i[:-4]],binance_balance[i[:-4]],max_ask_quantity,binance_bid_quantity)
        binance_sell_buy('limit', i, 'sell', sell_price[sell_exchange], trade_quantity)
        max_sell_buy(i,'buy',buy_price[buy_exchange],trade_quantity)
    elif sell_exchange == 'binance' and buy_exchange == 'kraken':#幣安賣 kraken買
        trade_quantity = min(kraken_balance[i[:-4]],binance_balance[i[:-4]],kraken_a_quantity,binance_bid_quantity)
        binance_sell_buy('limit', i, 'sell', sell_price[sell_exchange], trade_quantity)
    elif sell_exchange == 'max' and buy_exchange == 'binance':#max賣 幣安買
        trade_quantity = min(max_balance[i[:-4]],binance_balance[i[:-4]],max_bid_quantity,binance_ask_quantity)
        binance_sell_buy('limit', i, 'buy', buy_price[buy_exchange], trade_quantity)
        max_sell_buy(i, 'sell', sell_price[sell_exchange], trade_quantity)
    elif sell_exchange == 'max' and buy_exchange == 'kraken':#max賣 kraken買
        trade_quantity = min(max_balance[i[:-4]],kraken_balance[i[:-4]],max_bid_quantity,kraken_a_quantity)
        max_sell_buy(i, 'sell', sell_price[sell_exchange], trade_quantity)
    elif sell_exchange == 'kraken' and buy_exchange == 'max':#kraken賣 max買
        trade_quantity = min(max_balance[i[:-4]],kraken_balance[i[:-4]],max_ask_quantity,kraken_b_quantity)
        max_sell_buy(i, 'buy', buy_price[buy_exchange], trade_quantity)
    elif sell_exchange == 'kraken' and buy_exchange == 'binance':#kraken賣 幣安買
        trade_quantity = min(binance_balance[i[:-4]],kraken_balance[i[:-4]],binance_ask_quantity,kraken_b_quantity)
        binance_sell_buy('limit', i, 'buy', buy_price[buy_exchange], trade_quantity)
    
   

net_profit = {'LINKUSDT':0, 'ADAUSDT':0, 'XRPUSDT':0,'MATICUSDT':0,'SOLUSDT':0,'DOTUSDT':0,'LTCUSDT':0,'DOGEUSDT':0}
tradable_time = {'LINKUSDT':0, 'ADAUSDT':0, 'XRPUSDT':0,'MATICUSDT':0,'SOLUSDT':0,'DOTUSDT':0,'LTCUSDT':0,'DOGEUSDT':0}
exchange_sell = {'binance' : 0 ,'max' : 0,'kraken' : 0}
exchange_buy = {'binance' : 0 ,'max' : 0,'kraken' : 0}

binance_trading_pair = ['LINKUSDT', 'ADAUSDT', 'XRPUSDT','MATICUSDT','SOLUSDT','DOTUSDT','LTCUSDT','DOGEUSDT']
kraken_trading_pair = ['LINKUSDT', 'ADAUSDT', 'XRPUSDT','MATICUSDT','SOLUSDT','DOTUSDT','LTCUSDT','DOGEUSDT']

binance_balance = {'LINK':0, 'ADA':0, 'XRP':0,'MATIC':0,'SOL':0,'DOT':0,'LTC':0,'DOGE':0,'USDT':0}
kraken_balance = {'LINK':0, 'ADA':0, 'XRP':0,'MATIC':0,'SOL':0,'DOT':0,'LTC':0,'DOGE':0,'USDT':0}
max_balance = {'LINK':0, 'ADA':0, 'XRP':0,'MATIC':0,'SOL':0,'DOT':0,'LTC':0,'DOGE':0,'USDT':0,'TWD':0}

total_start_time = time.time()
hourly_check_time = time.time()

while True:
    try:
        print('需輸入交易所密鑰')
        #max
        m_api_key = ''
        m_api_secret = ''
        max_client = m_client(m_api_key, m_api_secret)
        
        #幣安
        client = Client(api_key='', 
                      api_secret='')
        
        #幣安查餘額
        binance_check_balance()
        #max查餘額
        max_check_balance()
    
        kraken_last_price = {}
        
        time.sleep(1)
        # 設置參數
        symbol = ['LINKUSDT', 'MATICUSDT','SOLUSDT']
        
        #計算總執行時間
        start_time = time.time()
        #幣安取得報價
        tickers = client.get_orderbook_tickers()
        
        #max取得報價
        response = requests.get("https://max-api.maicoin.com/api/v2/tickers")
        
        
        # kraken取得報價
        base_url = 'https://api.kraken.com/0/public/Ticker'
        symbols_str = ','.join(symbol)
        kraken_price_resp = requests.get(f"{base_url}?pair={symbols_str}")
        
        for i in symbol:
            params = {'symbol': i}
            #幣安取得報價
            binance_get_price()
            
            #max取得報價
            max_get_price()
            

            sell_price = {'binance' : binance_bid_price,'kraken' : kraken_b, 'max' : max_bid_price}
            buy_price = {'binance' : binance_ask_price,'kraken' : kraken_a, 'max' : max_ask_price}
            fee_rates = {'binance': 0.00075, 'max': 0.0005, 'kraken': 0.0016}
            market_fee_rates = {'binance': 0.00075, 'max': 0.0015, 'kraken': 0.0026}
            sell_exchange = max(sell_price, key = sell_price.get)
            buy_exchange = min(buy_price, key=buy_price.get)
            
            single_net_profit = (sell_price[sell_exchange]*(1-fee_rates[sell_exchange]) - buy_price[buy_exchange]*(fee_rates[buy_exchange]+1))
    
            #幣安買 k賣
            if single_net_profit > 0 :
                buy_sell()
                net_profit[i] += (single_net_profit * trade_quantity)
                tradable_time [i] += 1
                exchange_sell[sell_exchange] += 1
                exchange_buy[buy_exchange] += 1
                print(single_net_profit)
                print("最高的買單價 (kraken_b):", kraken_b)
                print("最高買單的數量 (kraken_b_quantity):", kraken_b_quantity)
                print("最低的賣單價 (kraken_a):", kraken_a)
                print("最低賣單的數量 (kraken_a_quantity):", kraken_a_quantity)
                print("Binance 最高買單價:", binance_bid_price)
                print("Binance 最高買單數量:", binance_bid_quantity)
                print("Binance 最低賣單價:", binance_ask_price)
                print("Binance 最低賣單數量:", binance_ask_quantity)
                print(f"max {i} 最高買單價: {max_bid_price}")
                print(f"max {i} 最高買單數量: {max_bid_quantity}")
                print(f"max {i} 最低賣單價: {max_ask_price}")
                print(f"max {i} 最低賣單數量: {max_ask_quantity}")
                print('smtp 缺少google雙重驗證應用程式密碼')
                smtp(f"net_profit : {net_profit}\n tradable_time : {tradable_time}\n exchange_buy : {exchange_buy} \n exchange_sell : {exchange_sell}")

        # 取得 Binance 伺服器的當前時間
        server_time = client.get_server_time()
        timestamp = server_time['serverTime']
        
        # 設定時間戳與伺服器時間的誤差，保護措施
        client.timestamp_offset = server_time['serverTime'] - int(time.time() * 1000)
        

        # 計算執行時間
        end_time = time.time()
        execution_time = end_time - start_time

        
        #計算總執行時間
        total_time_seconds = end_time - total_start_time
    
        # 轉換成天、小時、分鐘和秒
        days, remainder = divmod(total_time_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, seconds = divmod(remainder, 60)
        print(f"\n\n程式執行總時間: {int(days)} 天, {int(hours)} 小時, {int(minutes)} 分鐘, {int(seconds)} 秒.")
        current_time = time.time()
        if current_time - hourly_check_time >= 3600:  # 3600 秒等於一小時
            # 在這裡加入你想要每小時執行一次的操作
            smtp(f"net_profit : {net_profit}\n tradable_time : {tradable_time}\n exchange_buy : {exchange_buy} \n exchange_sell : {exchange_sell}")
            net_profit = {'LINKUSDT':0, 'ADAUSDT':0, 'XRPUSDT':0,'MATICUSDT':0,'SOLUSDT':0,'DOTUSDT':0,'LTCUSDT':0,'DOGEUSDT':0}
            tradable_time = {'LINKUSDT':0, 'ADAUSDT':0, 'XRPUSDT':0,'MATICUSDT':0,'SOLUSDT':0,'DOTUSDT':0,'LTCUSDT':0,'DOGEUSDT':0}
            exchange_buy = {'binance' : 0 ,'max' : 0,'kraken' : 0}
            exchange_sell = {'binance' : 0 ,'max' : 0,'kraken' : 0}
            
            # 更新每小時檢查的時間
            hourly_check_time = current_time
    except Exception as e:
        exception_info = traceback.format_exc()
        print(f"報錯：{exception_info}")
        time.sleep(30)