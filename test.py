import requests
import os
from dotenv import load_dotenv
load_dotenv()
# from binance.client import Client
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


image_gen('code')
