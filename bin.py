import json 
import requests 

key = "https://api.binance.com/api/v3/ticker/price?symbol="

asset_name = (input("Enter Coin Name : "))

url = key + asset_name
data = requests.get(url) 
data = data.json() 
print(data)
#print(f"{data['symbol']} price is {data['price']}") 
