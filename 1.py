import pandas
import re


def get_a_week_teachers():
    rasp_text1 = pandas.read_excel('downloaded_file.xlsx', index_col=0, usecols="B:L", skiprows=1)
    rasp_text1_str = rasp_text1.to_string()
    rasp_text1_lst = rasp_text1_str.split("\n")
    cl_list = []
    for item in rasp_text1_lst:
        item_s = re.sub(r'\s+', ' ', item)
        cl_list.append(item_s)

    del cl_list[0]
    new_cl_list = [] # массив из уроков для каждого класса их 47
    for list1 in cl_list:
        new_list = list1.split(" ")
        new_cl_list.append(new_list)
    len_list2 = len(teachers)

    list_new = [[] for _ in range(len_list2)]

    teacher_index = {}
    for i in range(len_list2):
        teacher_index[str(i + 1)] = i
    k = 1
    for lesson_classes in new_cl_list:
        # номер урока

        # print(lesson_classes)

        for lesson_class in lesson_classes:
            start_index = lesson_class.rfind('(')  # Находим индекс начала круглых скобок
            end_index = lesson_class.rfind(')')  # Находим индекс конца круглых скобок
            num_teacher = 0
            if start_index != -1 and end_index != -1:
                str1 = f"{k}. {lesson_class} - Класс {lesson_classes.index(lesson_class)+1} \n"
                num_teacher = int(lesson_class[start_index + 1:end_index])
                list_new[num_teacher-1].append(str1)
        k = k + 1
    #         teacher_number = 0
    #         if all(x == lesson_classes[0] for x in lesson_classes):
    #             return
    #         if lesson_class[-3] == "(":
    #             teacher_number = lesson_class[-2]
    #         else:
    #             teacher_number = lesson_class[-3:-1]
    #         if teacher_number in teacher_index:
    #             index = teacher_index[teacher_number]
    #             # номер класса
    #             i = lesson_classes.index(lesson_class) + 1
    #             str1 = f"{k}. " + lesson_class + f" - Класс {i}\n"
    #             # if lesson_class == lesson_classes[-1]:
    #             #     print("shdbfjshbfjus")
    #             #     k = k + 1
    #             k = k + 1
    #             print(str1)
    #             list_new[index].append(f"{k}. " + lesson_class + f" - Класс {i}\n")
    #
    #     # print(list_new)
    # list_lesson = "\n".join(["".join(sublist) for sublist in list_new])
    for item in list_new:
        print(item)


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


teachers = get_teachers_from_excel()



# print(get_a_week_students())
get_a_week_teachers()
