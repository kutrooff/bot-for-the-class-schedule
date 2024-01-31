import time
import telebot
from telebot import types
import requests
from urllib.parse import urlencode
import pandas
import schedule


bot = telebot.TeleBot('')


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


schedule.every().day.at("04:50").do(download_file)
schedule.every().day.at("8:00").do(download_file)


@bot.message_handler(commands=['start'])
def start(message):
    list1 = []
    keyboard = types.InlineKeyboardMarkup()
    for i in range(1, 12):
        btn_kgp = types.InlineKeyboardButton(
            text=f'Класс {i}',
            callback_data=str(i)

        )
        list1.append(btn_kgp)
    keyboard.add(*list1)
    bot.send_message(message.chat.id, "Привет, выберите класс: ", reply_markup=keyboard)


@ bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    if call.data == "return back":
        start(call.message)
    else:
        callback_data = int(call.data)
        callback_groups(call, callback_data)


def callback_groups(call, class_number):
    bot.send_message(call.message.chat.id, f"Расписание для {class_number} класса.")
    keyboard = types.InlineKeyboardMarkup()
    colms = [0, class_number]
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    rasp_text1 = rasp_text1.fillna('')
    rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    lines = rasp_text1_str.split('\n')
    filter_lines = [line for line in lines if not line.strip().endswith(("1.", "2.", "3.", "4.", "5.", "6.", "7."))]
    for i in range(len(filter_lines)):
        if filter_lines[i].strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
            filter_lines[i] = "      " + filter_lines[i]
    rasp_text1_str = "\n".join(filter_lines)
    bot.send_message(call.message.chat.id, rasp_text1_str)

    btn_return = types.InlineKeyboardButton(
        text='Вернуться назад',
        callback_data='return back'
    )
    keyboard.add(btn_return)
    bot.send_message(call.message.chat.id, "Нажмите кнопку...", reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, '''/start - запуск бота, 
/support - написать в поддержку
/contact - контакты разработчика ''')


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
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(3)



