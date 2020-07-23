import telebot
from telebot import types
from collections import defaultdict
import sqlite3

token = '1098632551:AAFWxP9r6bQ4HTfZ54Rcau3kBAC0qMOcS00'
bot = telebot.TeleBot(token)
add_plase = ['добавить', 'add', 'прикрепить']
list_plase = ['отобразить', 'показ', 'list']
reset_plase = ['очистить', 'reset', 'удалить', 'удаление']
START, TITLE, LOCKEYSHN, PICTCHE, CONFIRM = range(5)
USER_STATE = defaultdict(lambda: START)

PLACE = defaultdict(lambda: {})
USER_PPLACE = defaultdict(lambda: {})


def set_user_place(chat_id, title, lok, photo):
    USER_PPLACE[chat_id][title] = [lok, photo]
def get_user_place(chat_id):
    return USER_PPLACE[chat_id]
def reset(chat_id):
    print(type(USER_PPLACE[chat_id]))
    USER_PPLACE[chat_id].clear()


def update_lok(user_id, key, value):
    PLACE[user_id][key] = [value]

def get_place(user_id):
    return PLACE[user_id]


def get_state(message):
    return USER_STATE[message.chat.id]

def set_state(message, state):
    USER_STATE[message.chat.id] = state

def create_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width = 3)
    button = [
        types.InlineKeyboardButton(text = 'добавить', callback_data = '/add'),
        types.InlineKeyboardButton(text = 'отобразить', callback_data = '/list'),
        types.InlineKeyboardButton(text = 'очистить', callback_data = '/reset'),
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



@bot.message_handler(commands = ['list'])
@bot.message_handler(func = check_list)
def handle_message(message):
    print(message.text)
    chat_id = message.chat.id
    list_chat = USER_PPLACE[chat_id]
    bot.send_message(chat_id = message.chat.id,
                     text = "Вывод списка мест:")
    for title, value in list_chat.items():
        text = title
        chat_id = message.chat.id
        lok = value[0]
        photo = value[1]
        a = lok.longitude
        b = lok.latitude

        bot.send_message(chat_id = chat_id, text = text)
        bot.send_location(chat_id, b, a)


@bot.message_handler(commands = ['reset'])
@bot.message_handler(func = check_reset)
def handle_message(message):
    print(message.text)
    chat_id = message.chat.id
    reset(chat_id)
    bot.send_message(chat_id = message.chat.id, text = "Удаление всей информации")

@bot.message_handler(commands = ['add'])
@bot.message_handler(func = check_add)
def handle_message(message):
    print(message.text)
    set_state(message, TITLE)
    bot.send_message(chat_id = message.chat.id, text = "Добавление места в память. Название места!")

@bot.message_handler(func = lambda message: get_state(message) == TITLE)
def handle_message(message):
    print(message.text)
    update_lok(message.chat.id, 'title', message.text)
    bot.send_message(chat_id = message.chat.id,
                     text = "Добавление места в память. Загрузи локацию!")
    set_state(message, LOCKEYSHN)

@bot.message_handler(func = lambda message: get_state(message) == START)
def handle_message(message):
    print(message.text)
    keyboard = create_keyboard()
    bot.send_message(chat_id = message.chat.id,
                     text = "Что нужно сделать",
                     reply_markup =keyboard)


@bot.callback_query_handler(func = lambda x: True)
def callback_handler(callback_query):
    mess = callback_query.message
    text = callback_query.data
    print(mess.chat.id)
    print(text)
    text = 'введи: ' + str(text)
    bot.send_message(mess.chat.id, text = text)


@bot.message_handler(func = lambda message: get_state(message) == PICTCHE,
                     content_types=['photo'])
def handle_docs_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

    except Exception as e:
        bot.reply_to(message, e)

    bot.reply_to(message, "Фото добавлено, все правильно?")
    image = open(src, 'rb')
    bot.send_photo(message.chat.id, image, caption = 'test')
    update_lok(message.chat.id, 'photo', src)

    pl = get_place(message.chat.id)
    bot.send_message(chat_id = message.chat.id,
                     text = 'All - {}'.format(pl))
    set_state(message, CONFIRM)


@bot.message_handler(func = lambda message: get_state(message) == LOCKEYSHN,
                     content_types = 'location')
def handle_message(message):
    print(message.location)
    update_lok(message.chat.id, 'lok', message.location)
    bot.send_message(chat_id = message.chat.id,
                     text = "Добавление места в память. Загрузи фото!")
    set_state(message, PICTCHE)

@bot.message_handler(func = lambda message: get_state(message) == CONFIRM)
def handle_message(message):
    print(message.location)
    if "da" in message.text.lower():
        bot.send_message(chat_id = message.chat.id,
                         text = 'Добавлено')
        pl = get_place(message.chat.id)
        set_user_place(message.chat.id, pl['title'][0], pl['lok'], pl['photo'])
        set_state(message, START)


if __name__ == '__main__':
    bot.polling()

