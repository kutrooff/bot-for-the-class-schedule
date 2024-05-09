import re

# Исходная строка
s = "bhjsjdhb          jsgdfhswegf                    wefygwuf                                iuhefihwife     shfs"

# Удаление лишних пробелов и замена их на один пробел
cleaned_string = re.sub(r'\s+', ' ', s)

# Вывод результата
print(cleaned_string)
