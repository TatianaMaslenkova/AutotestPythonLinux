import yaml
import pytest

from Seminar2_func import checkout_negative

with open('config.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)


class TestNegative:
    def test_step1(self, make_folder, clear_folder, make_files, create_bad_archive):  # e извлекли из архива
        # test1
        assert checkout_negative(f"cd {data['folderbad']}; 7z e arx2.7z -o{data['folderext']} -y",
                                 "ERRORS"), "test1 FAIL"

    def test_step2(self, make_folder, clear_folder, make_files,
                   create_bad_archive):  # t проверка целостности архива
        # test2
        assert checkout_negative(f"cd {data['folderbad']}; 7z t arx2.7z", "Is not")


if __name__ == '__main__':
    pytest.main(['-vv'])
