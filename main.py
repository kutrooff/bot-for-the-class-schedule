import time
import telebot
from telebot import types
import requests
from urllib.parse import urlencode
import pandas
import schedule
import numpy as np
import re
import datetime
import os

bot = telebot.TeleBot('6027502149:AAFA_0K0zqTdwAcHCDiV9kLh7fB8c7h9qiw')


def download_file():
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    public_key = 'https://disk.yandex.ru/i/xEBQolhFeC5D4g'
    # Получаем загрузочную ссылку
    final_url = base_url + urlencode(dict(public_key=public_key))
    response = requests.get(final_url)
    download_url = response.json()['href']
    # Загружаем файл и сохраняем его
    download_response = requests.get(download_url)
    file_path = 'downloaded_file.xlsx'
    with open(file_path, 'wb') as f:
        f.write(download_response.content)


def job():
    download_file()


schedule.every().day.at("04:50").do(job)
schedule.every().day.at("13:00").do(job)


class User:
    def __init__(self, role, text_user):
        self.role = role
        self.text_user = text_user

    def get_role(self):
        return self.role

    def get_text_user(self):
        return self.text_user



def get_teachers_from_excel():
    df = pandas.read_excel("downloaded_file.xlsx", index_col=0, usecols="O:O", skiprows=1)
    df = str(df)
    df = df.replace(", nan", "")
    string = df
    start_index = string.rfind('[')  # Находим индекс начала квадратных скобок
    end_index = string.rfind(']')  # Находим индекс конца квадратных скобок
    if start_index != -1 and end_index != -1:
        substring = string[start_index + 1:end_index]  # Используем срез для получения строки между квадратными скобками
        df = substring.split(", ")
    return df
# Словарь для хранения объектов пользователей
def get_a_week_students():
    # keyboard = types.InlineKeyboardMarkup()
    rasp_text1 = pandas.read_excel('downloaded_file.xlsx', index_col=0, usecols="B:L", skiprows=1)
    rasp_text1_str = rasp_text1.to_string()
    rasp_text1_lst = rasp_text1_str.split("\n")

    cl_list = []
    for item in rasp_text1_lst:
        item_s = re.sub(r'\s+', ' ', item)
        cl_list.append(item_s)

    del cl_list[0]

    classes_list = [[], [], [], [], [], [], [], [], [], [], []]

    for i in range(len(cl_list)):
        list1 = cl_list[i].split(" ")
        for i in range(len(list1)):
            classes_list[i].append(list1[i])

    pattern = r'(Naц\s*)+'

    # Применяем замену к каждому элементу внутренних списков
    for i in range(len(classes_list)):
        classes_list_str = ' '.join(classes_list[i])
        classes_list_str = re.sub(pattern, 'NaN ', classes_list_str)
        # После замены преобразуем строку обратно в список
        classes_list[i] = classes_list_str.split()

    sort_item = []
    for item in classes_list:
        sort_item.append("\n".join(item))

    all_rasp = []
    for item in sort_item:
        if item == sort_item[0]:
            item = "\n" + item
        all_rasp.append(item.split("NaN"))

    for sublist in all_rasp:
        for i, line in enumerate(sublist):
            # Разделение строки по символу '\n' и удаление пустых строк
            subjects = [subj.strip() for subj in line.split('\n') if subj.strip()]

            # Пронумерование и сбор строк
            new_line = ""
            for j, subj in enumerate(subjects, 1):
                new_line += f"{j}. {subj}\n"

            # Замена строки в исходном списке измененной строкой
            sublist[i] = new_line

    teachers = get_teachers_from_excel()
    schedule = all_rasp
    new_schedule = []  # Создаем новый список для модифицированных строк
    for group_schedule in schedule:
        new_group_schedule = []  # Создаем новый список для модифицированных строк в текущем списке расписания
        for item in group_schedule:
            subjs = item.split("\n")
            new_subjs = []  # Создаем новый список для модифицированных предметов в текущей строке
            for subj in subjs:
                start_index = subj.rfind('(')  # Находим индекс начала круглых скобок
                end_index = subj.rfind(')')  # Находим индекс конца круглых скобок
                if start_index != -1 and end_index != -1:
                    num_teacher = int(subj[start_index + 1:end_index])
                    new_subj = subj[:start_index] +" — "+ teachers[num_teacher - 1]  # Заменяем подстроку
                    new_subjs.append(new_subj)
                else:
                    new_subjs.append(subj)  # Если круглых скобок нет, просто добавляем предмет без изменений
            new_group_schedule.append(
                "\n".join(new_subjs))  # Объединяем модифицированные предметы в одну строку и добавляем в новый список
        new_schedule.append(new_group_schedule)  # Добавляем новый список расписания для текущей группы в общий список
    # print(new_schedule)
    return new_schedule


# def get_a_week_teachers():
#     rasp_text1 = pandas.read_excel('downloaded_file.xlsx', index_col=0, usecols="B:L", skiprows=1)
#     rasp_text1_str = rasp_text1.to_string()
#     rasp_text1_lst = rasp_text1_str.split("\n")
#     print(rasp_text1_lst)
#
#
#
# a = get_a_week_teachers()

# print(a)
users = {}
all_rasp_for_students = get_a_week_students()


# Функция для получения или создания объекта пользователя
def get_or_create_user(user_id, role, text_user):
    if user_id not in users:
        users[user_id] = User(role, text_user)
    else:
        users[user_id].role = role
        users[user_id].text_user = text_user





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


def get_buttons(call):
    keyboard = [
        [types.InlineKeyboardButton("Сегодня", callback_data='on_today')],
        [types.InlineKeyboardButton("Завтра", callback_data='on_tomorrow')],
        [types.InlineKeyboardButton("На неделю", callback_data='on_week')]
    ]
    reply_markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(call.message.chat.id, "Получить расписание на:", reply_markup=reply_markup)


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


def delete_all_messages(call):
    bot.delete_message(call.message.chat.id, call.message.message_id - 1)

    # try:
    #     # Получение всех сообщений в чате
    #     messages = bot.sent_messages
    #
    #     # Удаление каждого сообщения, отправленного ботом
    #     for message in messages:
    #         if message.chat.id == chat_id:
    #             bot.delete_message(chat_id, message.message_id)
    #
    #     # Оповещение об удалении сообщений
    #     bot.send_message(chat_id, "Все предыдущие сообщения были удалены.")
    # except Exception as e:
    #     print("Ошибка при удалении сообщений:", e)


def get_rasp_on_week(class_index):
    rasps = all_rasp_for_students
    class_index -= 1
    count_day = 0

    # Список дней недели
    days_of_week = ['Понедельник:', 'Вторник:', 'Cреда:', 'Четверг:', 'Пятница:', 'Суббота:', "Воскресенье"]

    # Проверяем, что группа с таким индексом существует в списке rasps
    if class_index < len(rasps):
        # Проверяем, что день недели существует в расписании для данной группы
        # if count_day < len(rasps[class_index]):
        str_rasp = ""
        for item in rasps[class_index]:
            if count_day == 6:
                str_rasp += days_of_week[count_day] + "\n" + "Выходной"
                return str_rasp
            str_rasp += days_of_week[count_day] + "\n" + item + "\n"
            count_day += 1
    # else:
    #     return "День недели не найден в расписании для этой группы"
    else:
        return "Группа не найдена в расписании"


def get_rasp_today_or_tomorrow(class_index, tomorrow):
    rasps = all_rasp_for_students
    class_index -= 1
    # Получаем текущий день недели
    today = datetime.datetime.today().weekday()

    if tomorrow:
        today += 1

    if today == 7:
        today = 0
    # Список дней недели
    days_of_week = ['Понедельник:', 'Вторник:', 'Cреда:', 'Четверг:', 'Пятница:', 'Суббота:', "Воскресенье"]
    # print(f"class_index:{class_index}")
    # Проверяем, что группа с таким индексом существует в списке rasps
    if class_index < len(rasps):
        # Проверяем, что день недели существует в расписании для данной группы
        if today < len(rasps[class_index]):
            if today == 6:
                return days_of_week[today] + "\n" + "Выходной"
            return days_of_week[today] + "\n" + rasps[class_index][today]
        else:
            return "День недели не найден в расписании для этой группы"
    else:
        return "Группа не найдена в расписании"


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'teacher':
        send_teacher_options(call)
    elif call.data == 'student':
        send_student_options(call)
    elif 'Класс ' in call.data:
        # print(users)
        get_or_create_user(call.from_user.id, "Ученик", call.data)
        # print(users)
        # delete_all_messages(call)
        bot.send_message(call.message.chat.id, "Ваши настройки сохранены")
        get_buttons(call)
    elif call.data == "on_today":
        id = call.from_user.id
        # print(call.from_user.id)
        # print(users[id].get_role())
        # print(users[id].get_text_user())
        if users[id].get_role() == "Ученик":
            match = re.search(r'Класс (\d+)', users[id].get_text_user())
            class_index = int(match.group(1))
            # print(f"cl:{class_index}")
            rasp = get_rasp_today_or_tomorrow(class_index, False)

            bot.send_message(call.message.chat.id, rasp)
    elif call.data == "on_tomorrow":
        id = call.from_user.id
        if users[id].get_role() == "Ученик":
            match = re.search(r'Класс (\d+)', users[id].get_text_user())
            class_index = int(match.group(1))
            # print(f"cl:{class_index}")
            rasp = get_rasp_today_or_tomorrow(class_index, True)

            bot.send_message(call.message.chat.id, rasp)
    elif call.data == "on_week":
        id = call.from_user.id
        if users[id].get_role() == "Ученик":
            match = re.search(r'Класс (\d+)', users[id].get_text_user())
            class_index = int(match.group(1))
            # print(f"cl:{class_index}")
            rasp = get_rasp_on_week(class_index)
            # print(rasp)
            bot.send_message(call.message.chat.id, rasp)


@bot.callback_query_handler(func=lambda call: True)
def callback_querry(call):
    if call.data == "return back":
        start(call.message)
    else:
        callback_data = int(call.data)
        # get_a_week(call, callback_data)

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
            # print(e)
            time.sleep(3)
