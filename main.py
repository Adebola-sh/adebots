import os
import telebot
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv
from extras import START_MSG_CONTENT, SARCASTIC_MSG, get_crypto, gaming, image_gen, client
from random import choice


# ============== Initializations ===============
load_dotenv('auth.env')
API_key=os.getenv('key')
bot=telebot.TeleBot(API_key)
COUNTER = 0

print('running')
# ================ Late importations ==================


###---- Assigning the content of the joke.txt and the yo mama file ----###

with open('./texts/jokes.txt', 'r') as jk:
    all_yo = jk.readlines()
with open('./texts/short_jokes.txt', 'r') as sjk:
    all_sjk = sjk.read().split('..!')

##########******** ------ ALL USEABLE TEXTS HERE ------********##########
text_messages = {
    'welcome':
        'Please welcome {name}!\n to the group, he got added here by @{admin}',
    'info':
        f'My name is {bot.get_me().username},\n'
        'I am a bot that assists these wonderful group chat members\n'
        "with simple and complex tasks. Type '/start' to"
        f'see all commands. {START_MSG_CONTENT}'}

##########******** ------ ALL BOT COMMANDS STARTS HERE ------********##########

@bot.message_handler(commands=['start', 'hello'])
def start(message):
    global COUNTER
    COUNTER+=1
    if COUNTER%2==0:
        start_msg=bot.reply_to(message,
            SARCASTIC_MSG)
    else:
        start_msg = bot.reply_to(message,
            START_MSG_CONTENT.format(username=message.from_user.username))
    print(f'{message.text} called')

@bot.message_handler(commands=['help'])
def on_info(message):
    bot.reply_to(message, text_messages['info'])

@bot.message_handler(commands=['greet'])
def greet(message):
    """The bot greets you. It is more like the ping command with a simpler operation"""
    bot.send_message(message.chat.id,
        f'what\'s up with you @{message.from_user.username}, how are you doing?')

crypto_pairs = ['BTCUSDT', 'BNBUSDT', 'ETHUSDT', 'ARBUSDT', 'SUIUSDT', 'AVAXUSDT', 'SOLUSDT']

@bot.message_handler(commands=['ping'])
def ping(message):
    """This function exists to check if the bot is active or not. 
    To prove that it is alive, it respond by returning
    the current UTC+1 time and price of a random cryptocurrency
    from the list given above"""

    pair = choice(crypto_pairs)
    coin = pair.strip('USDT')
    result = get_crypto(pair)
    bot.reply_to(message, f"""I'm alive 👀😁 the time is {result['timenow']}...😉😎😎
    hey {message.from_user.username}\n\n
{coin} current price is: {result['price']} 📊 \nThe percentage today is :{result['price_change']} %\n\n
The Current Volume being traded on Binance is {result['vol']} {coin}.
Amountuing to: {result['quote']} USDT 🐳💸""")
    print(f'{message.text} called')

@bot.message_handler(commands=['members'])
def mem_count(message):
    """This returns the number of members currently on a group. it returns 2 in dm"""
    mem = bot.get_chat_members_count(message.chat.id)
    if mem < 3:
        bot.reply_to(
            message,
            f'only {mem} of us are present in this chat now')
    else:
        bot.reply_to(
    message,
    f'{mem} members are present in this group now')

@bot.message_handler(commands=['yomama'])
def yoMama(message):
    bot.send_message(message.chat.id, f'😂💀 {choice(all_yo)}😂🤣💀💀')
    print(f'{message.text} called')


@bot.message_handler(commands=['joke'])
def joke(message):
    bot.reply_to(message, f'{choice(all_sjk)}😂🤣💀💀')

##########****** ------ ALL BOT COMMANDS ENDS HERE ------******##########
#------------------------------------------------------------------------
#######**** ------ ALL MISCELLANEOUS FUNCTIONS ARE HERE ------****#######

#id_list=[1806862179, 2106703150,1871663191]
#k=[bot.send_message(i,f'Hello @Fundsman ... 😂💀 {choice(all_sjk)}😂🤣💀💀') for i in id_list]

    #binance_timestamp=client.get_server_time()
    #pinging = str(datetime.fromtimestamp(binance_timestamp['serverTime']/1000)).split('.')[0]
#-------------------------------------------------------------------------
#########***** ----- ALL BOT MESSAGE CHECK STARTS HERE -----*****#########

@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def on_user_joins(message):
    """This function listen for an event of new members joining the group"""
    for user in message.json["new_chat_members"]:
        bot.send_message(
            message.chat.id,
            text_messages['welcome'].format(
                name=user['first_name'],
                admin=message.from_user.username
                )
            )



@bot.message_handler(func=lambda message:True, content_types=['text','dice'])
def determine_msg_type(message):
    if message.content_type == 'text':
        if message.text.lower() in  ['play', 'dice']:
            gaming(message)
        elif message.text.lower().startswith('price'):
            pair_msg(message)
        elif 'new here' in message.text:
            bot.reply_to(message,
                'hey welcome, click on /start or /help to navigate through my usage')
    elif message.content_type == 'dice':
        gaming(message)
def pair_msg(message):
    pairs = message.text.split()
    if len(pairs) ==1:
        bot.reply_to(message,
            "No pair given ⚠  try using price followed by the symbol, e.g price btcusdt")
    pair = pairs[1].upper()
    try:
        info = client.get_klines(symbol=pair, interval='2h', limit=1 )
        info0 = info[0]
        bot.reply_to(message, 
            f"""hey @{message.from_user.username},
the last 2 hr candle for {pair} has:\n
open:{info0[1]} 📊
\nHigh: {info0[2]} 📈 \n
low: {info0[3]} 📉 \n
close: {info0[4]}📊 \n
volume traded: {info0[5]} 🐳 \n
and No. of {pairs[1].split()[0]}
traded on Binance 1hr ago: {info0[8]} 💸💷""")
    except BinanceAPIException as error_found:
        if error_found.message == "Invalid symbol.":
            bot.reply_to(message,
                f'''{pair} is not a valid currency 🔎 \n
                or it\'s not available in our database'''
                )
    except Exception:
        pass

@bot.edited_message_handler(func=lambda message:True)
def caught(message):
    bot.reply_to(message,
        'Heyyo, hope no problem? you edited your message...\n we can Discuss in my Dm if you don\'t mind')

@bot.message_handler(func=lambda message:True, content_types=['sticker', 'emoji'])
def sticker_reply(message):
    with open('stickers.txt', 'a+') as stk:
        stk.seek(0)
        if (message.sticker.file_id) not in stk:
            stk.write(message.sticker.file_id+'\n')
            stk.seek(0)
        else:
            pass
        random_pick = stk.readlines()
    print(message.sticker.file_id)
    bot.send_sticker(message.chat.id, sticker=choice(random_pick).strip('\n'))

def listener(messages):
    for message in messages:
        print(f'a message received,  Content_type: {message.content_type}')
bot.set_update_listener(listener)
bot.infinity_polling()
