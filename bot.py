import telebot
from telebot import types


token = '1098632551:AAFWxP9r6bQ4HTfZ54Rcau3kBAC0qMOcS00'
bot = telebot.TeleBot(token)
currecies = ['кнопка 1', 'кнопка 2', 'кнопка - !2,.']
ver = 2

def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width = 2)
    button = [types.InlineKeyboardButton(text = c, callback_data = c) for c in currecies]
    keyboard.add(*button)
    return keyboard

def check_currency(message):
    if message.text:
        for c in currecies:
            if c in message.text.lower():
                return True
        return False
    return False

@bot.message_handler(func = check_currency)
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id = message.chat.id, text = "ok"+str(ver))

@bot.message_handler(commands = ['rate', 'pate'])
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id = message.chat.id, text = "rate - pate"+str(ver))


@bot.message_handler(commands = ['we'])
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id = message.chat.id, text = "we"+str(ver))

@bot.message_handler()
def handle_message(message):
    print(message.text)
    keyboard  = create_keyboard()
    bot.send_message(chat_id = message.chat.id, text = "we2"+str(ver), reply_markup =keyboard )

@bot.callback_query_handler(func = lambda x:True)
def callback_handler(callback_query):
    mess = callback_query.message
    text = callback_query.data
    print(mess.chat.id)
    print(text)
    bot.send_message(mess.chat.id, text = text)
    bot.answer_callback_query(callback_query.id, text)



@bot.message_handler(content_types = 'location')
def handle_message(message):
    print(message.location)
    a = {}
    a['longitude'] = message.location.longitude
    a['latitude'] = message.location.latitude
    bot.send_message(chat_id = message.chat.id, text = (str(a['longitude'])+ str(a['latitude'])))
    bot.send_location(message.chat.id, a['longitude'], a['latitude'] )
print('start')
bot.polling()
