import datetime
import requests
import json
import pandas as pd
import mplfinance as mpf




api_key = 'your_api_key'
api_secret = 'your_api_secret'

# Define the start and end times for the data
end_time = datetime.datetime.now()
start_time = end_time - datetime.timedelta(days=365)

# Convert the times to Unix timestamps in milliseconds
start_timestamp = int(start_time.timestamp() * 1000)
end_timestamp = int(end_time.timestamp() * 1000)

# Define the Binance API endpoint for K-line data
endpoint = 'https://api.binance.com/api/v3/klines'

# Define the parameters for the API request
symbol = 'BTCUSDT'
interval = '15m'
limit = 1000
params = {'symbol': symbol, 'interval': interval, 'startTime': start_timestamp, 'endTime': end_timestamp, 'limit': limit}

# Send the API request and store the response data in a list
data = []
while True:
    response = requests.get(endpoint, params=params)
    klines = json.loads(response.text)
    data += klines
    if len(klines) < limit:
        break
    params['startTime'] = int(klines[-1][0]) + 1
    #datetime.time.sleep(0.1)

# Create a pandas dataframe with the OHLC data and timestamps
ohlc_data = [[float(kline[1]), float(kline[2]), float(kline[3]), float(kline[4])] for kline in data]
df = pd.DataFrame(ohlc_data, columns=['Open', 'High', 'Low', 'Close'])
timestamps = [datetime.datetime.fromtimestamp(int(kline[0]) / 1000) for kline in data]
df['Timestamp'] = timestamps
df.set_index('Timestamp', inplace=True)

# Define the style for the plot
style = mpf.make_mpf_style(base_mpf_style='charles', rc={'font.size': 8})

# Create the OHLC plot
mpf.plot(df[-50:], type='candle', style=style, title='BTC/USDT OHLC', ylabel='Price ($)')