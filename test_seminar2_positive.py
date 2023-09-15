import yaml
import pytest
from Seminar2_func import checkout
import subprocess

"""
ДЗ 3. Задание 1. Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее 
созданный файл stat.txt строку вида: время, кол-во файлов из конфига, размер файла из конфига, 
статистика загрузки процессора из файла /proc/loadavg (можно писать просто всё содержимое этого файла).
Задание 2. Дополнить все тесты ключом команды 7z -t (тип архива). Вынести этот параметр в конфиг.
"""

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_add_archive(self, make_folder, clear_folder, make_files):  # a создали архив
        res_add = checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok")
        res_ls = checkout(f'ls {data["folderout"]}', f'arx2.{data["type"]}')
        assert res_add and res_ls

    def test_check_e_extract(self, clear_folder, make_files):  #
        res = list()
        res.append(
            checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(
            checkout(f'cd {data["folderout"]}; 7z e arx2.{data["type"]} -o{data["folderext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext"]}', item))

        assert all(res)

    def test_check_e_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(
            checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(
            checkout(f'cd {data["folderout"]}; 7z e arx2.{data["type"]} -o{data["folderext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext"]}', item))
        for item in make_subfolder:
            res.append(checkout(f'ls {data["folderext"]}', item))

        assert all(res)

    def test_check_x_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        # files, subflder and files in subfolder
        res = list()
        res.append(
            checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(
            checkout(f'cd {data["folderout"]}; 7z x arx2.{data["type"]} -o{data["folderext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext"]}', item))

        res.append(checkout(f'ls {data["folderext"]}', make_subfolder[0]))
        res.append(checkout(f'ls {data["folderext"]}/{make_subfolder[0]}', make_subfolder[1]))

        assert all(res)

    def test_check_x_files(self, clear_folder, make_files):  # only files
        res = list()
        res.append(
            checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(
            checkout(f'cd {data["folderout"]}; 7z x arx2.{data["type"]} -o{data["folderext3"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext3"]}', item))
        assert all(res)

    def test_totality(self, clear_folder, make_files):  # t проверка целостности архива
        res = list()
        res.append(
            checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z t arx2.{data["type"]}', "Everything is Ok"))

        assert all(res)

    def test_delete(self, clear_folder, make_files, make_subfolder):  # d удаление из архива
        res = list()
        res.append(
            checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z d arx2.{data["type"]}', "Everything is Ok"))

        assert all(res)

    def test_update(self):  # u - обновление архива
        assert checkout(f'cd {data["folderin"]}; 7z u {data["folderout"]}/arx2.{data["type"]}',
                        "Everything is Ok"), 'NO update'

    def test_nonempty_archive(self, clear_folder, make_files):
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z l arx2.{data["type"]}', f'{len(make_files)} files'))

    def test_check_hash(self, make_folder, clear_folder, make_files):
        checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok")
        result = subprocess.run(f"crc32 {data['folderout']}/arx2.{data['type']}", shell=True,
                                stdout=subprocess.PIPE, encoding='utf-8')
        assert checkout(f"cd {data['folderout']}; 7z h arx2.{data['type']}",
                        f"{result.stdout.rstrip().upper()}"), "Hash is not equal"


if __name__ == "__main__":
    pytest.main(['--v'])
