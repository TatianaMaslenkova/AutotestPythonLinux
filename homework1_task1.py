import subprocess

"""
Написать функцию на Python, которой передаются в качестве параметров команда и текст.
Функция должна возвращать True, если команда успешно выполнена и текст найден в её выводе и False
в противном случае. Передаваться должна только одна строка, разбиение вывода использовать не нужно.
"""


def find_text(command_name, text):
    result = subprocess.run(command_name, shell=True, stdout=subprocess.PIPE, encoding="utf-8")
    if result.returncode == 0:
        res = result.stdout
        if text in res:
            return True
        else:
            return False


command1 = "cat /etc/os-release"
text1 = "jammy"
text2 = "22.04.1"
print(find_text(command1, text1))
print(find_text(command1, text2))
