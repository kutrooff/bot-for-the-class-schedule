import time
import telebot
from telebot import types

# со временем может кидать ошибку
# хотя до этого работало
# решение - удалить и заново установить pytelegrambotapi, т.е.
# pip reinstall pytelegrambotapi
# pip install pytelegrambotapi

bot = telebot.TeleBot('6724361419:AAGOgTf4eamG4bgwKGAfMAbaepxG0kVIQbc')

#создаем команду
@bot.message_handler(commands=['start']) 
def start(message):
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()

    # кнопка 8 класса
    btn_keygroup11 = types.InlineKeyboardButton(
        text='Класс «11»',
        callback_data='11'
    )
    btn_keygroup10 = types.InlineKeyboardButton(
        text='Класс «10»',
        callback_data='10'
    )
    btn_keygroup9 = types.InlineKeyboardButton(
        text='Класс «9»',
        callback_data='9'
    )
    btn_keygroup8 = types.InlineKeyboardButton(
        text='Класс «8»',
        callback_data='8'
    )
    btn_keygroup7 = types.InlineKeyboardButton(
        text='Класс «7»',
        callback_data='7'
    )
    btn_keygroup6 = types.InlineKeyboardButton(
        text='Класс «6»',
        callback_data='6'
    )
    btn_keygroup5 = types.InlineKeyboardButton(
        text='Класс «5»',
        callback_data='5'
    )
    btn_keygroup4 = types.InlineKeyboardButton(
        text='Класс «4»',
        callback_data='4'
    )
    btn_keygroup3 = types.InlineKeyboardButton(
        text='Класс «3»',
        callback_data='3'
    )
    btn_keygroup2 = types.InlineKeyboardButton(
        text='Класс «2»',
        callback_data='2'
    )
    btn_keygroup1 = types.InlineKeyboardButton(
        text='Класс «1»',
        callback_data='1'
    )
    keyboard.add(btn_keygroup11)
    keyboard.add(btn_keygroup10)
    keyboard.add(btn_keygroup9)
    keyboard.add(btn_keygroup8)
    keyboard.add(btn_keygroup7)
    keyboard.add(btn_keygroup6)
    keyboard.add(btn_keygroup5)
    keyboard.add(btn_keygroup4)
    keyboard.add(btn_keygroup3)
    keyboard.add(btn_keygroup2)
    keyboard.add(btn_keygroup1)
    bot.send_message(message.chat.id, "Выберите класс", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_group(call):
    if call.data == '11' or call.data == '10' or call.data == '9' or call.data == '8' or call.data == '7' or call.data == '6' or call.data == '5':
    #call.data это callback_data, которую мы указали при объявлении кнопки
        #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, "Расписание для всех классов.")

        # клавиатура
        keyboard = types.InlineKeyboardMarkup()

        # кнопки
        btn_week_1 = types.InlineKeyboardButton(
            text='1-ая неделя',
            callback_data='week_1'
        )
        keyboard.add(btn_week_1)

        btn_week_2 = types.InlineKeyboardButton(
            text='2-ая неделя',
            callback_data='week_2'
        )
        keyboard.add(btn_week_2)

        bot.send_message(call.message.chat.id, "Выберите неделю...", reply_markup=keyboard)

    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    if call.data == 'week_1':
    #call.data это callback_data, которую мы указали при объявлении кнопки
        with open('C:\\Users\\Nikolai\\Desktop\\telebot\\text\\rasp_week_1.txt', 'r', encoding='utf-8') as f:
            rasp_text = f.read()
        #код сохранения данных, или их обработки
        bot.send_message(
            call.message.chat.id, rasp_text, reply_markup=keyboard)
    elif call.data == 'week_2':
        with open('C:\\Users\\Nikolai\\Desktop\\telebot\\text\\rasp_week_2.txt', 'r', encoding='utf-8') as f:
            rasp_text = f.read()
        #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, rasp_text, reply_markup=keyboard)


bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)