from Seminar2_func import checkout
import subprocess

"""
Добавить в проект тесты, проверяющие работу команд d (удаление из архива) и u (обновление 
архива). Вынести в отдельные переменные пути к папкам с файлами, с архивом и с распакованными 
файлами. Выполнить тесты с ключом -v."""

folderin = "/home/user/tst"
folderout = "/home/user/out"
folderext = "/home/user/folder1"
folderext2 = "/home/user/folder2"


def test_step1():
    # test1
    assert checkout(f"cd {folderin}; 7z a {folderout}/arx2", "Everything is Ok"), "test1 FAIL"


def test_step2():
    # test2
    assert checkout(f"cd {folderout}; 7z e arx2.7z -o{folderext} -y", "Everything is Ok"), "test2 FAIL"


def test_step3():
    # test3
    assert checkout(f"cd {folderout}; 7z t arx2.7z", "Everything is Ok"), "test3 FAIL"


def test_step4():
    # test4
    assert checkout(f"cd {folderout}; 7z d arx2.7z", "Everything is Ok"), "test4 FAIL"


def test_step5():
    # test5
    assert checkout(f"cd {folderin}; 7z u {folderout}/arx2.7z", "Everything is Ok"), "test5 FAIL"


"""
Доработать позитивные тесты таким образом, чтобы при архивации дополнительно проверялось 
создание файла архива, а при распаковке проверялось создание файлов.
"""


def test_step6():
    # test6
    res1 = checkout(f"cd {folderin}; 7z a {folderout}/arx2", "Everything is Ok")
    res2 = checkout(f"ls {folderout}", "arx2.7z")
    assert res1 and res2, "test6 FAIL"


def test_step7():
    # test7
    res1 = checkout(f"cd {folderout}; 7z e arx2.7z -o{folderext} -y", "Everything is Ok"), "test7 FAIL"
    res2 = checkout(f"ls {folderext}", "test1.txt")
    res3 = checkout(f"ls {folderext}", "test2.txt")
    assert res1 and res2 and res3, "test7 FAIL"


"""
ДЗ 2. Задача 1. Дополнить проект тестами, проверяющими команды вывода списка файлов (l) и 
разархивирования с путями (x).
"""


def test_step8():
    # test8
    assert checkout(f"cd {folderout}; 7z l arx2.7z", "2 files")


def test_step9():
    # test9
    assert checkout(f"cd {folderout}; 7z x arx2.7z -o{folderext2} -y", "Everything is Ok"), "test9 FAIL"


"""
ДЗ 2. Задача 2. Установить пакет для расчёта crc32. Доработать проект, добавив тест команды 
расчёта хеша (h). Проверить, что хеш совпадает с рассчитанным командой crc32.
"""


def test_step10():
    # test10
    result = subprocess.run("crc32 /home/user/out/arx2.7z", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
    print(result)
    assert checkout(f"cd {folderout}; 7z h arx2.7z", f"{result.stdout.rstrip().upper()}"), "test10 FAIL"
