import yaml
import pytest
from Seminar2_func import checkout
import subprocess

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


class TestPositive:

    def test_add_archive(self, make_folder, clear_folder, make_files):  # a создали архив
        res_add = checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok")
        res_ls = checkout(f'ls {data["folderout"]}', "arx2.7z")
        assert res_add and res_ls

    def test_check_e_extract(self, clear_folder, make_files):  #
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z e arx2.7z -o{data["folderext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext"]}', item))

        assert all(res)

    def test_check_e_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z e arx2.7z -o{data["folderext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext"]}', item))
        for item in make_subfolder:
            res.append(checkout(f'ls {data["folderext"]}', item))

        assert all(res)

    def test_check_x_extract_subfolder(self, clear_folder, make_files, make_subfolder):
        # files, subflder and files in subfolder
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z x arx2.7z -o{data["folderext"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext"]}', item))

        res.append(checkout(f'ls {data["folderext"]}', make_subfolder[0]))
        res.append(checkout(f'ls {data["folderext"]}/{make_subfolder[0]}', make_subfolder[1]))

        assert all(res)

    def test_check_x_files(self, clear_folder, make_files):  # only files
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z x arx2.7z -o{data["folderext3"]} -y', "Everything is Ok"))
        for item in make_files:
            res.append(checkout(f'ls {data["folderext3"]}', item))
        assert all(res)

    def test_totality(self, clear_folder, make_files):  # t проверка целостности архива
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z t arx2.7z', "Everything is Ok"))

        assert all(res)

    def test_delete(self, clear_folder, make_files, make_subfolder):  # d удаление из архива
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z d arx2.7z', "Everything is Ok"))

        assert all(res)

    def test_update(self):  # u - обновление архива
        assert checkout(f'cd {data["folderin"]}; 7z u {data["folderout"]}/arx2.7z', "Everything is Ok"), 'NO update'

    def test_nonempty_archive(self, clear_folder, make_files):
        res = list()
        res.append(checkout(f'cd {data["folderin"]}; 7z a {data["folderout"]}/arx2', "Everything is Ok"))
        res.append(checkout(f'cd {data["folderout"]}; 7z l arx2.7z', f'{len(make_files)} files'))

    def test_check_hash(self):
        result = subprocess.run("crc32 /home/user/out/arx2.7z", shell=True, stdout=subprocess.PIPE, encoding='utf-8')
        assert checkout(f"cd {data['folderout']}; 7z h arx2.7z", f"{result.stdout.rstrip().upper()}"), "FAIL"


if __name__ == "__main__":
    pytest.main(['--v'])
