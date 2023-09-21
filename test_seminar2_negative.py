import pytest

from ssh_checkers import ssh_checkout, ssh_checkout_negative, ssh_getout, upload_files
import yaml

with open('config.yaml') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def save_log(self, start_time, name):
        with open(name, 'a') as f:
            f.write(ssh_getout(data["ip"], data["user"], data["passwd"], f"journalctl --since '{start_time}'"))

    def test_deploy(self, start_time):
        res = []
        upload_files(data["ip"], data["user"], data["passwd"], f'tests/{data["pkgname"]}.deb',
                     f'/home/{data["user"]}/{data["pkgname"]}.deb')
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f'echo "{data["passwd"]}" | sudo -S dpkg -i /home/{data["user"]}/{data["pkgname"]}.deb',
                                "Настраивается пакет"))
        res.append(ssh_checkout(data["ip"], data["user"], data["passwd"],
                                f'echo "{data["passwd"]}" | sudo -S dpkg -s {data["pkgname"]}',
                                "Status: install ok installed"))
        self.save_log(start_time, "log_negative.txt")
        assert all(res), "test_deploy FAIL"

    def test_negative1(self, make_folder, clear_folder, make_files, create_bad_archive,
                       start_time):  # e извлекли из архива
        self.save_log(start_time, "log_negative.txt")
        assert ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                     f'cd {data["folderbad"]}; 7z e arx2.{data["type"]} -o{data["folderext"]} -y',
                                     "ERRORS")

    def test_negative2(self, make_folder, clear_folder, make_files, create_bad_archive,
                       start_time):  # t проверка целостности архива
        self.save_log(start_time, "log_negative.txt")
        assert ssh_checkout_negative(data["ip"], data["user"], data["passwd"],
                                     f'cd {data["folderbad"]}; 7z t arx2.{data["type"]}', "Is not")


if __name__ == '__main__':
    pytest.main(['-v'])
