import telebot
from telebot import types


token = '1098632551:AAFWxP9r6bQ4HTfZ54Rcau3kBAC0qMOcS00'
bot = telebot.TeleBot(token)
add_plase = ['добавить', 'add', 'прикрепить' ]
list_plase = ['отобразить', 'показ', 'list']
reset_plase = ['очистить', 'reset', 'удалить', 'удаление']
ver = 2
add_flag = False


def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width = 3)
    button = [
        types.InlineKeyboardButton(text = 'добавить место', callback_data = '/add+'),
        types.InlineKeyboardButton(text = 'отобразить список', callback_data = '/list+'),
        types.InlineKeyboardButton(text = 'очистить все места', callback_data = '/reset+'),
              ]
    keyboard.add(*button)
    return keyboard

def check_add(message):
    if message.text:
        for c in add_plase:
            if c in message.text.lower():
                return True
        return False
    return False

def check_list(message):
    if message.text:
        for c in list_plase:
            if c in message.text.lower():
                return True
        return False
    return False

def check_reset(message):
    if message.text:
        for c in reset_plase:
            if c in message.text.lower():
                return True
        return False
    return False


@bot.message_handler(commands = ['add'])
@bot.message_handler(func = check_add)
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id = message.chat.id, text = "Добавление места в память. Загрузи локацию!")



@bot.message_handler(commands = ['list'])
@bot.message_handler(func = check_list)
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id = message.chat.id, text = "Вывод списка мест")

@bot.message_handler(commands = ['reset'])
@bot.message_handler(func = check_reset)
def handle_message(message):
    print(message.text)
    bot.send_message(chat_id = message.chat.id, text = "Удаление всей информации")

@bot.message_handler()
def handle_message(message):
    print(message.text)
    keyboard = create_keyboard()
    bot.send_message(chat_id = message.chat.id,
                     text = "Что нужно сделать",
                     reply_markup =keyboard)

@bot.callback_query_handler(func = lambda x:True)
def callback_handler(callback_query):
    mess = callback_query.message
    text = callback_query.data
    print(mess.chat.id)
    print(text)

    bot.send_message(mess.chat.id, text = text)




@bot.message_handler(content_types = 'location')
def handle_message(message):
    print(message.location)
    a = {}
    a['longitude'] = message.location.longitude
    a['latitude'] = message.location.latitude
    bot.send_message(chat_id = message.chat.id, text = (str(a['longitude'])+ str(a['latitude'])))
    bot.send_location(message.chat.id, a['longitude'], a['latitude'] )


if __name__ == '__main__':
    bot.polling()

