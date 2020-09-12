import telebot
import sqlite3
import time

from config import TOKEN, FLAG

bot = telebot.TeleBot(TOKEN, threaded=False)

hello_en = "Hello, "
hello_ru = "Привет, "
hello_jp = "こんにちは, "

callback_options = {"en": hello_en, "ru": hello_ru, "jp": hello_jp}

start_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
en = telebot.types.InlineKeyboardButton('EN', callback_data="en")
ru = telebot.types.InlineKeyboardButton('RU', callback_data="ru")
jp = telebot.types.InlineKeyboardButton('JAPANESE', callback_data="jp")
start_markup.row(en, ru)
start_markup.row(jp)


def init_db():
    # ...
    # some boring sql stuff here

    # add super users
    c.execute("INSERT INTO users VALUES (0, '{}')".format(FLAG))
    c.execute("INSERT INTO users VALUES (1, '{}')".format("Mister quote"))
    conn.commit()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id

    try:
        name = message.from_user.first_name + " " + message.from_user.last_name
    except TypeError:
        bot.send_message(chat_id, "Sry, I don't know your full name, fix your account and type /start again")
        return

    query = "INSERT INTO users VALUES ('{}', '{}')".format(chat_id, name)
    try:
        c.executescript(query)
    except sqlite3.Error as sql_e:
        if "no such table" in str(sql_e):
            init_db()
            bot.send_message(chat_id, "Please type /start again")
            return

    conn.commit()
    bot.send_message(chat_id, "Привет, выбери язык на котором тебя поприветствовать", reply_markup=start_markup)


@bot.callback_query_handler(func=lambda call: True)
def test_callback(call):
    callback = call.data

    bot.answer_callback_query(callback_query_id=call.id, text='OK!', cache_time=0)

    try:
        username = c.execute("SELECT name FROM users WHERE id={}".format(str(call.from_user.id))).fetchone()
    except sqlite3.Error:
        username = ("Anon",)

    bot.send_message(call.from_user.id, callback_options[callback] + username[0] if username else "Anon")


if __name__ == "__main__":
    conn = sqlite3.connect('task.db')
    c = conn.cursor()
    init_db()

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(1)
