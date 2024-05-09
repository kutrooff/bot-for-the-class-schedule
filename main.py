import time
import telebot
from telebot import types
import requests
from urllib.parse import urlencode
import pandas
import schedule
import numpy as np
import re

bot = telebot.TeleBot('6350527159:AAFA5ceDIZ4DJNuBhoTFDh67lSMJFdYjxcQ')


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


def job():
    download_file()


schedule.every().day.at("04:50").do(job)
schedule.every().day.at("13:00").do(job)


class User:
    def __init__(self, user_id, role, text_user):
        self.user_id = user_id
        self.role = role
        self.text_user = text_user

    def multiply(self):
        return f"{self.user_id} и {self.role} и {self.text_user}"


# Словарь для хранения объектов пользователей
users = {}


# Функция для получения или создания объекта пользователя
def get_or_create_user(user_id, role, text_user):
    if user_id not in users:
        users[user_id] = User(user_id, role, text_user)
    else:
        users[user_id].role = role
        users[user_id].text_user = text_user
    print(users[user_id].multiply())


def get_teachers_from_excel():
    file_loc = 'C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx'
    df = pandas.read_excel(file_loc, index_col=0, usecols="O:O", skiprows=1)
    df = str(df)
    df = df.replace(", nan", "")
    string = df
    start_index = string.rfind('[')  # Находим индекс начала квадратных скобок
    end_index = string.rfind(']')  # Находим индекс конца квадратных скобок
    if start_index != -1 and end_index != -1:
        substring = string[start_index + 1:end_index]  # Используем срез для получения строки между квадратными скобками
        df = substring.split(", ")
    return df


def send_teacher_options(call):
    teachers = get_teachers_from_excel()
    list1 = []
    keyboard = types.InlineKeyboardMarkup()
    for teacher in teachers:
        btn_kgp = types.InlineKeyboardButton(
            text=teacher,
            callback_data=teacher
            # callback_data=str[i]
        )
        list1.append(btn_kgp)
    keyboard.add(*list1)
    bot.send_message(call.message.chat.id, "Привет, выберите ФИО: ", reply_markup=keyboard)


def send_student_options(call):
    list1 = []
    keyboard = types.InlineKeyboardMarkup()
    for i in range(1, 12):
        btn_kgp = types.InlineKeyboardButton(
            text=f'Класс {i}',
            callback_data=f'Класс {i}'
            # callback_data=str[i]
        )
        list1.append(btn_kgp)
    keyboard.add(*list1)
    bot.send_message(call.message.chat.id, "Привет, выберите класс: ", reply_markup=keyboard)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = [
        [types.InlineKeyboardButton("Учитель", callback_data='teacher')],
        [types.InlineKeyboardButton("Ученик", callback_data='student')]
    ]
    reply_markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, "Привет, выберите роль: ", reply_markup=reply_markup)
    # user = get_or_create_user(user_id)
    # update.message.reply_text('Выберите роль:', reply_markup=reply_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'teacher':
        # Отправляем выборку для учителя
        send_teacher_options(call)
    elif call.data == 'student':
        # Отправляем выборку для ученика
        send_student_options(call)
    elif 'Класс ' in call.data:
        get_or_create_user(call.from_user.id, "Ученик", call.data)
        class_num = int(call.data[6:])
        get_a_week(call, class_num)
    elif call.data:
        print(call.data)


# @bot.callback_query_handler(func=lambda call: True)
# def callback_query(call):
#     print(call.data)
#     user_id = call.from_user.id
#     class_selected = call.data
#     get_or_create_user(user_id, "Ученик", class_selected)


@bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    if call.data == "return back":
        start(call.message)
    else:
        callback_data = int(call.data)
        get_a_week(call, callback_data)


def get_a_week(call, class_number):
    keyboard = types.InlineKeyboardMarkup()
    rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', index_col=0, usecols="B:L", skiprows=1)
    rasp_text1_str = rasp_text1.to_string()
    rasp_text1_lst = rasp_text1_str.split("\n")

    cl_list = []
    for item in rasp_text1_lst:
        item_s = re.sub(r'\s+', ' ', item)
        cl_list.append(item_s)

    del cl_list[0]


    cl_list = [line for line in cl_list if not all(word == 'NaN' for word in line.split())]

    classes_list = [[],[],[],[],[],[],[],[],[],[],[]]
    print(len(cl_list))
    for i in range(len(cl_list)):
        list1 = cl_list[i].split(" ")
        for i in range(len(list1)):
            classes_list[i].append(list1[i])

    print(classes_list)

    # for i in range(11):
    #     list_classes[i] = []
    #     for j in range(6):
    #         list_classes[i][j] = []

    # for item in rasp_text1_lst:
    #     item = re.sub(r'\s+', ' ', item)
    # print(rasp_text1_lst)
    #     if item == "":
    #         rasp_text1_lst.remove(item)
    # cleaned_lines = [line for line in rasp_text1_lst if "NaN" not in line]
    # cleaned_lines.pop(0)

    # for item in rasp_text1_lst:
    #     list1 = item.split(" ")
    #     print(list1)
    # Вывод результата
    # print(cleaned_lines)

    # rasp_text1_lst.pop(0)
    # for i in range(11):
    #     rasp_text1_lst.pop(i)

    # colms = [0, class_number]
    # rasp_text1 = pandas.read_excel('C:\\Users\\Nikolai\\Desktop\\telebot\\downloaded_file.xlsx', usecols=colms)
    # rasp_text1 = rasp_text1.fillna('')
    # rasp_text1_str = rasp_text1.to_string(index=False).replace(" ", "")
    # lines = rasp_text1_str.split('\n')
    # filter_lines = [line for line in lines if not line.strip().endswith(("1.", "2.", "3.", "4.", "5.", "6.", "7."))]
    # copy_filter_lines = filter_lines
    # filter_lines.pop(0)
    # # for i in range(len(filter_lines)):
    # #     try:
    # #         print(int(filter_lines[i][0])
    # #     except ValueError:
    # #         filter_lines.pop(i)
    #
    # for i in range(len(filter_lines)):
    #     if filter_lines[i].strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.")):
    #         filter_lines[i] = "      " + filter_lines[i]
    # rasp_text1_str = "\n".join(filter_lines)
    # filter_lines.pop(0)
    # print(filter_lines)
    # schedule_week = rasp_text1_str
    # # print(schedule_week)
    # bot.send_message(call.message.chat.id, schedule_week)

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
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(e)
            time.sleep(3)
