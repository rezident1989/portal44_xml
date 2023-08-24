import os
import zipfile
from src.config.config_colorama import GREEN, RESET
from src.helper.help_func import clear_folder

clear_folder('test')
count_all = 0
count_res = 0
for i in os.listdir('server_2'):
    count_all += 1
    with zipfile.ZipFile(f"server_2/{i}", "r") as myzip:
        for file_info in myzip.infolist():
            if file_info.filename.endswith('.xml'):
                count_all += 1
                string = ('penalties')
                byte_object = string.encode("utf-8")
                if byte_object in myzip.read(file_info):
                    count_res += 1
                    if count_res != 0:
                        break
                    myzip.extract(file_info, path='test')

print(f'Проверено XML: {GREEN}{count_all}{RESET}')
print(f'Найдено XML: {GREEN}{count_res}{RESET}')
