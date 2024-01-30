import time
import telebot
from telebot import types
import requests
from urllib.parse import urlencode
import pandas
import schedule


bot = telebot.TeleBot('6724361419:AAGOgTf4eamG4bgwKGAfMAbaepxG0kVIQbc')


def download_file():
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = 'https://disk.yandex.ru/i/xEBQolhFeC5D4g'
    # Получаем загрузочную ссылку
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    # Загружаем файл и сохраняем его
    download_response = requests.get(download_url)
    with open('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', 'wb') as f:
        f.write(download_response.content)


schedule.every().day.at("09:00").do(download_file)
schedule.every().day.at("19:00").do(download_file)


@bot.message_handler(commands=['start'])
def start(message):

    keyboard = types.InlineKeyboardMarkup()
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
    keyboard.add(btn_keygroup1, btn_keygroup2, btn_keygroup3, btn_keygroup4, btn_keygroup5, btn_keygroup6, btn_keygroup7, btn_keygroup8, btn_keygroup9, btn_keygroup10, btn_keygroup11)

    bot.send_message(message.chat.id, "Привет, выберите класс: ", reply_markup=keyboard)


@ bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    if call.data == "1":
        callback_group1(call)
    elif call.data == "2":
        callback_group2(call)
    elif call.data == "3":
        callback_group3(call)
    elif call.data == "4":
        callback_group4(call)
    elif call.data == "5":
        callback_group5(call)
    elif call.data == "6":
        callback_group6(call)
    elif call.data == "7":
        callback_group7(call)
    elif call.data == "8":
        callback_group8(call)
    elif call.data == "9":
        callback_group9(call)
    elif call.data == "10":
        callback_group10(call)
    elif call.data == "11":
        callback_group11(call)
    elif call.data == "return back":
        start(call.message)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '''/start - запуск бота, 
/support - написать в поддержку
/contact - контакты разработчика ''')


def callback_group1(call):
    bot.send_message(call.message.chat.id, "Расписание для 1 класса.")
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 1]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group2(call):

    bot.send_message(call.message.chat.id, "Расписание для 2 класса.")
    keyboard = types.InlineKeyboardMarkup()
    # клавиатура
    colms = [0, 2]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group3(call):
    bot.send_message(call.message.chat.id, "Расписание для 3 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 3]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group4(call):
    bot.send_message(call.message.chat.id, "Расписание для 4 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 4]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group5(call):
    bot.send_message(call.message.chat.id, "Расписание для 5 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 5]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group6(call):
    bot.send_message(call.message.chat.id, "Расписание для 6 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 6]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group7(call):
    bot.send_message(call.message.chat.id, "Расписание для 7 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 7]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group8(call):
    bot.send_message(call.message.chat.id, "Расписание для 8 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 8]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group9(call):
    bot.send_message(call.message.chat.id, "Расписание для 9 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 9]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group10(call):
    bot.send_message(call.message.chat.id, "Расписание для 10 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 10]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


def callback_group11(call):
    bot.send_message(call.message.chat.id, "Расписание для 11 класса.")
    # клавиатура
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, 11]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    bot.send_message(call.message.chat.id, rasp_text1_str)
    # кнопка
    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


@bot.message_handler(commands=['contact'])
def send_contact(message):
    bot.send_message(message.chat.id, 'контакты разработчика - @nikktov')


    
@bot.message_handler(commands=['support'])
def send_support(message):
    bot.send_message(message.chat.id, 'проблемы с ботом или он не работает - пишите тг @nikktov')


bot.polling(none_stop=True, interval=0)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            time.sleep(3)
            print(e)

while True:
    schedule.run_pending()
    time.sleep(1)