import telebot
from telebot import types
from collections import defaultdict
import requests

token = '1098632551:AAFWxP9r6bQ4HTfZ54Rcau3kBAC0qMOcS00'
bot = telebot.TeleBot(token)
add_plase = ['добавить', 'add', 'прикрепить']
list_plase = ['отобразить', 'показ', 'list', 'покажи']
reset_plase = ['очистить', 'reset', 'удалить', 'удаление', 'стереть']

START, TITLE, LOCKEYSHN, PICTCHE, CONFIRM = range(5)
USER_STATE = defaultdict(lambda: START)

PLACE = defaultdict(lambda: {})
USER_PPLACE = defaultdict(lambda: {})


def google(origins, destinations=None):
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {'key': 'AIzaSyCMQMdjMGQUkqwbuFHb7axE2mVh_rTWDGU',
              'units': 'metric',
              'language': 'ru',
              'origins': '50.474455,30.511866',
              'destinations': '50.474455,30.511866',
              }
    if destinations:
        params['origins'] = origins
        params['destinations'] = destinations
    else:
        params['origins'] = origins
        params['destinations'] = origins

    r = requests.get(url, params = params)
    q = r.json()
    distance = q['rows'][0]['elements'][0]['distance']
    addres = q['origin_addresses'][0]
    return addres, distance

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


@bot.callback_query_handler(func = lambda x: True)
def callback_handler(callback_query):
    mess = callback_query.message
    text = callback_query.data
    if text == '/add':
        handle_message_add(mess)
    elif text == '/list':
        handle_message_list(mess)
    elif text == '/reset':
        handle_message_reset(mess)


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
def handle_message_list(message):
    print(message.text)

    chat_id = message.chat.id
    list_chat = USER_PPLACE[chat_id]
    bot.send_message(chat_id = message.chat.id,
                     text = "Укажите текущую геолокацию для поиска мест в радиусе 500 м.")


@bot.message_handler(commands = ['reset'])
@bot.message_handler(func = check_reset)
def handle_message_reset(message):
    print(message.text)
    chat_id = message.chat.id
    reset(chat_id)
    bot.send_message(chat_id = message.chat.id, text = "Все сохраненные Вами места удалены!")

@bot.message_handler(commands = ['add'])
@bot.message_handler(func = check_add)
def handle_message_add(message):
    print(message.text)
    set_state(message, TITLE)
    bot.send_message(chat_id = message.chat.id, text = "Добавление места в память.")
    bot.send_message(chat_id = message.chat.id, text = "Введите название этого места!")


@bot.message_handler(func = lambda message: get_state(message) == START)
def handle_message_start(message):
    bot.send_message(chat_id = message.chat.id, text = " Здравствуйте!")
    bot.send_message(chat_id = message.chat.id, text = "Я - бот,который позволит сохранять места для будущего посещения")
    bot.send_message(chat_id = message.chat.id,
                     text = "Могу сохранить описание, локацию и фото необходимого места")
    bot.send_message(chat_id = message.chat.id,
                     text = "Могу показать все сохраненные места в радицсе 500м.")
    bot.send_message(chat_id = message.chat.id,
                     text = "Могу стереть все сохраненные Ваши записи.")

    keyboard = create_keyboard()
    bot.send_message(chat_id = message.chat.id,
                     text = "Что нужно сделать",
                     reply_markup =keyboard)


@bot.message_handler(func = lambda message: get_state(message) == TITLE)
def handle_message_title(message):
    print(message.text)
    update_lok(message.chat.id, 'title', message.text)
    bot.send_message(chat_id = message.chat.id,
                     text = "Загрузи локацию!")
    bot.send_message(chat_id = message.chat.id,
                     text = "(нажать 'скрепку', затем зелёненькая 'Location')")
    set_state(message, LOCKEYSHN)


@bot.message_handler(func = lambda message: get_state(message) == LOCKEYSHN,
                     content_types = 'location')
def handle_message_lok(message):
    lat = message.location.latitude
    lon = message.location.longitude
    coord = str(lat) + ',' + str(lon)
    update_lok(message.chat.id, 'lok', coord)
    text, dist = google(coord)
    bot.send_message(chat_id = message.chat.id,
                     text = text)
    bot.send_message(chat_id = message.chat.id,
                     text = "Загрузи фото!")
    set_state(message, PICTCHE)





@bot.message_handler(func = lambda message: get_state(message) == PICTCHE,
                     content_types=['photo'])
def handle_message_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = file_info.file_path
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

    except Exception as e:
        bot.reply_to(message, e)

    bot.reply_to(message, "Сохранить запись?")

    update_lok(message.chat.id, 'photo', src)

    pl = get_place(message.chat.id)

    set_state(message, CONFIRM)




@bot.message_handler(func = lambda message: get_state(message) == CONFIRM)
def handle_message_confirm(message):
    print(message.location)
    if "da" or 'yes' or 'да' or 'ok' or 'ок' in message.text.lower():
        bot.send_message(chat_id = message.chat.id,
                         text = 'Добавлено')
        pl = get_place(message.chat.id)
        set_user_place(message.chat.id, pl['title'][0], pl['lok'], pl['photo'])
        set_state(message, START)

@bot.message_handler(func = lambda message: get_state(message) == START,
                     content_types = 'location')
def handle_message_lok(message):
    lat = message.location.latitude
    lon = message.location.longitude
    local_coord = str(lat) + ',' + str(lon)

    chat_id = message.chat.id
    list_chat = USER_PPLACE[chat_id]
    count = 0
    for title, value in list_chat.items():
        text = title
        chat_id = message.chat.id
        lok = value[0]
        adres, dist = google(local_coord, lok)
        if int(dist['value']) <= 500:
            count += 1
            photo = value[1]
            image = open(photo[0], 'rb')
            a, b = lok[0].split(',')
            bot.send_message(chat_id = chat_id, text = text)
            bot.send_location(chat_id, a, b)
            bot.send_photo(chat_id, image)
    if count == 0:
        bot.send_message(chat_id = chat_id, text = 'Рядом не найдено ни одного места!')
    else:
        bot.send_message(chat_id = chat_id, text = 'Количество найденых рядом мест: {}!'.format(count))

if __name__ == '__main__':
    bot.polling()

