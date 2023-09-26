import os
import zipfile
from src.helper.help_func import clear_folder


def search_xml(*args):
    search_folder = f'ftp\\contract'

    test = list(map(lambda a: a.encode("utf-8"), args))
    print(test)
    clear_folder(os.path.join(os.path.expanduser('~'), 'Desktop', 'xml'))
    count_res = 0
    count = 0

    for i in os.listdir(f'../{search_folder}'):
        if count_res != 0:
            print('\nУра. Пакеты найдены!')
            break
        with zipfile.ZipFile(f"../{search_folder}/{i}", "r") as myzip:
            for file_info in myzip.infolist():
                if file_info.filename.endswith('.xml'):
                    count += 1
                    print(f'\rПроверено пакетов XML: {count}', end=' ')
                    if sum([1 for tag in test if tag in myzip.read(file_info)]) == len(test):
                        count_res += 1
                        myzip.extract(file_info, os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'xml'))
    if count_res == 0:
        print('\nПакеты не найдены(')


if __name__ == '__main__':
    search_xml('closedContract')
