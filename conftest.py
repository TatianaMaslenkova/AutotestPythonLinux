import random
import string
import yaml
import pytest
import subprocess
from Seminar2_func import checkout
from datetime import datetime

with open('config.yaml') as f:
    data = yaml.safe_load(f)


@pytest.fixture()
def make_folder():
    return checkout(
        f'mkdir -p {data["folderin"]} {data["folderout"]} {data["folderext"]} {data["folderext3"]} {data["folderbad"]} '
        f'{data["logfolder"]}', "")


@pytest.fixture()
def clear_folder():
    return checkout(
        f'rm -rf {data["folderin"]}/* {data["folderout"]}/* {data["folderext"]}/* {data["folderext3"]}/* '
        f'{data["folderbad"]}/*', "")


@pytest.fixture()
def make_files():
    list_files = []
    for i in range(data['count']):
        file_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
        checkout(f'cd {data["folderin"]}; dd if=/dev/urandom of={file_name} bs={data["bs"]} count=1 iflag=fullblock',
                 '')
        list_files.append(file_name)

    return list_files


@pytest.fixture()
def make_subfolder():
    subfolder_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    subfile_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
    if not checkout(f'cd {data["folderin"]}; mkdir {subfolder_name}', ''):
        return None, None
    if not checkout(f'cd {data["folderin"]}/{subfolder_name}; '
                    f'dd if=/dev/urandom of={subfile_name} bs={data["bs"]} count=1 iflag=fullblock', ''):
        return subfolder_name, None

    return subfolder_name, subfile_name


@pytest.fixture()
def create_bad_archive():
    checkout(f'cd {data["folderin"]}; 7z a -t{data["type"]} {data["folderout"]}/arx2', "Everything is Ok")
    checkout(f'cp {data["folderout"]}/arx2.{data["type"]} {data["folderbad"]}', '')
    checkout(f'truncate -s 1 {data["folderbad"]}/arx2.{data["type"]}', '')  # сделали битым


@pytest.fixture(autouse=True)
def print_time():
    print("Start: {}".format(datetime.now().strftime("%H:%M:%S.%f")))
    yield
    print(f'Finish: {datetime.now().strftime("%H:%M:%S.%f")}')


"""
ДЗ 3. Задание 1. Дополнить проект фикстурой, которая после каждого шага теста дописывает в заранее 
созданный файл stat.txt строку вида: время, кол-во файлов из конфига, размер файла из конфига, 
статистика загрузки процессора из файла /proc/loadavg (можно писать просто всё содержимое этого файла).
"""


@pytest.fixture(autouse=True)
def log_file():
    yield
    info = subprocess.run("cat /proc/loadavg", shell=True, stdout=subprocess.PIPE, encoding='utf-8').stdout
    checkout(f'cd {data["logfolder"]}; echo "time = {datetime.now().strftime("%H:%M:%S.%f")}", '
             f'files_count = {data["count"]}", size = {data["bs"]}, cpu_statistics = {info}" >> stat.txt', '')
