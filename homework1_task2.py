import subprocess
import string

"""
Доработать функцию из предыдущего задания таким образом, чтобы у нее появился дополнительный режим работы, 
в котором вывод разбивается на слова с удалением всех знаков пунктуации (их можно взять из списка 
string.punctuation модуля string). В этом режиме должно проверяться наличие слова в выводе.
"""


def find_text(command_name, text, add_mode=False):
    result = subprocess.run(command_name, shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    res = result.stdout
    if add_mode:
        check_punct = res.translate(str.maketrans('', '', string.punctuation)).split("\n")
        if result.returncode == 0:
            for el in check_punct:
                print(el)
                if text in el:
                    return True
            return False
    else:
        if text in res and result.returncode == 0:
            return True
        else:
            return False


command1 = "cat /etc/os-release"
text1 = "debian"
text2 = "Ubuntu"
text3 = "linux"
command2 = "rm --help"
text4 = "version"
print(find_text(command1, text1))
print(find_text(command1, text2))
print(find_text(command1, text3, add_mode=True))
print(find_text(command2, text4, add_mode=True))
