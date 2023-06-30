import os
import requests
import telebot
# from bi na nce client  Client
from pybit.unified_trading import HTTP
from datetime import datetime
from dotenv import load_dotenv
from time import sleep




# ====== Initializations ======= #
load_dotenv('auth.env')
API_key=os.getenv('key')
bot=telebot.TeleBot(API_key)
key = os.getenv('Bybit_Api_Key')
secret = os.getenv('Bybit_Api_Secret')
# client=Client()
client = HTTP(testnet = False, api_key=key, api_secret=secret)


# ========= Useful Variables ========= #
START_MSG_CONTENT = '''hello {username} ,you\'re welcome.
        Things I can do are numerous but some are: \n 
1)Tell funny jokes with /joke \n
2)Tell Yo mama jokes with /yomama \n
3)Tell Bitcoin current price (I\'m a Bitcoiner😎😎😉) with the /ping command \n
4)I can respond to the /greet command too \n
5) Get number of people in the group with /members
\n 6)know about me with /help \n
7)Type 'play' or 'dice' to play GAME with me
\n 8)Type 'price' followed by any coin pair, to get the price.\n
                e.g: price bnbusdt \n
9)I can beat you in a sticker battle... try me first😜😜😂
10)The most surprising is that you can Dm me😉'''

SARCASTIC_MSG = '''how many times do you want to start? 😂 \n
            well if you do that again, we\'ll have issues...\n lol I\'m kidding'''


# ========= Important Functions ========= #
def get_crypto(pair):
    """"This function gets Cryptocurrency prices from Bybit server.
    It doesnt have so much use, maybe it will in the future."""
    info = client.get_tickers(symbol=str(pair).upper(), category= 'spot')
    info = info['result']['list'][0]
    info1= info['symbol']
    price = info['lastPrice']
    change = info['price24hPcnt']
    vol = round(float(info['volume24h']),3)
    low24h = round(float(info["lowPrice24h"]),1)
    d= datetime.now()
    timenow=d.strftime('%A %X %p')
    return {
        'info': info, 'info1': info1,
        'price':price, 'price_change':change,
        'vol': vol, 'low24h': low24h, 'cur_time': d,
        'timenow': timenow
        }


def gaming(message):
    """This is the function that takes care of the gaming """
    total_my_score=[]
    total_bot_score=[]
    my_score= 0
    sleep(2)
    if message.content_type == 'dice':
        bot.reply_to(message, f'you, @{message.from_user.username} scored {message.dice.value}')
        my_score = message.dice.value
        total_my_score.append(message.dice.value)
    message_bot=bot.send_dice(message.chat.id)
    sleep(4)
    bot_score = message_bot.dice.value
    sleep(2)
    total_bot_score.append(message_bot.dice.value)

    if bot_score > my_score:
        bot.send_message(message.chat.id, 'boooooo😜😜🧨🔥🔥.... I won this round 🤸🏽‍♂️🤸🏽‍♂️')
        sleep(0.9)
        bot.send_sticker(
            message.chat.id,
            sticker='CAACAgQAAx0CVwhgoQACBq9iTEKV8_9VuVXYv4DQOk5xRcqe2gACcwoAAn0HmFDTPkeco6qRrSME'
            )
    elif bot_score == my_score:
        bot.send_message(message.chat.id, 'That was a tie 🤝🏽💪🏽↔')
    else:
        bot.send_message(message.chat.id, 'yooooo🧨🔥🔥🤸‍♂️🔥.... You won this round!!!')
    sleep(1.4)
    bot.send_message(message.chat.id, 'It\'s your turn to play ⏯ 🤸‍♂️')

    if len(total_my_score)==5:
        bot.send_message(
            message.chat.id,
            f"""We've come to the end of this session\n
                with @{message.from_user.username} having a total of {sum(total_my_score)}
                and I, {message_bot.from_user.first_name} got a total of {sum(total_bot_score)}.
                Best of luck!!!\n
                Type 'Dice' and CLICK on the DICE Icon to play again.""")
        total_bot_score.clear()
        total_my_score.clear()


def image_gen(object):
    base = 'https://api.unsplash.com/'
    response = requests.get(base)