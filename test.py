import requests
import os
from pybit.exceptions import InvalidRequestError as IRE
from pybit.unified_trading import HTTP
from dotenv import load_dotenv
load_dotenv('auth.env')
# from bina nce. clie nt import Client
# client = Client()
# info = client.get_klines(symbol='AVAXUSDT', interval='2h', limit=1)
# info0 = info[0]
access_key = os.getenv("UNSPLASH_PUBLIC_KEY")
def image_gen(query):
    endpoint = '/search/photos'
    home = f'https://api.unsplash.com/{endpoint}/'
    response = requests.get(home,timeout=20,
                params={'client_id':access_key, 'query': query, 'page':1, 'per_page':2})
    data = response.json()
    for pics in data['results']:
        print(pics['description'], pics['urls']['full'])
        print(pics['links']["download"])


# image_gen('code')

secret = os.getenv('Bybit_Api_Secret')
key = os.getenv('Bybit_Api_Key')
# base = "https://api-testnet.bybit.com"
# kline = base+'/v5/market/kline'

client = HTTP(testnet = False, api_key=key, api_secret=secret)

try:
    candle = client.get_kline(
        category="spot",
        symbol="BTCUSDC",
        interval=60,
        limit = 1
    )

    print(candle['result']['list'][0][6])
except IRE as error:
    print(error.message)
except Exception as p:
    print(p)
    pass
