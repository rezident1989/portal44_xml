import datetime
import time
import xml.etree.ElementTree as ET
from random import randint
import os
import paramiko
from password import password_sftp


def open_xml(path: str) -> ET.Element:
    """Открывает xml"""
    return ET.ElementTree(file=path).getroot()


def random_number(digits: int) -> str:
    """Сгенерировать случайное число"""
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    return str(randint(lower, upper))


def clear_folder(folder: str) -> None:
    """Очистить папку"""
    for file in os.listdir(os.path.abspath(f'{folder}')):
        os.remove(os.path.abspath(os.path.join(f'{folder}', file)))


def remove_file(file: str, folder: str) -> None:
    """Переместить папку"""
    os.replace(file, f"{folder}/{file.split('/')[-1:][0]}")


def get_type_xml(path: str) -> str:
    """Получить название пакета xml"""

    return open_xml(path).tag.split('}')[1]


def create_xml(tree: ET.Element) -> str:
    """Создает xml"""
    if 'export' == tree.tag.split('}')[1]:
        name_file = tree[0].tag.split('}')[1]
    else:
        name_file = 'confirmation'
    date_time = datetime.datetime.now().strftime("%H.%M_%d.%m.%y_")
    name = "".join(name_file).replace('}', '')
    path_name = f'incoming/{date_time}{name}.xml'
    tree = ET.ElementTree(tree)
    tree.write(path_name, encoding='utf-8', xml_declaration=True)

    return path_name


def to_sent_to_sftp(path, host):
    transport = paramiko.Transport(host)
    transport.connect(None, username='root', password=password_sftp)
    sftp = paramiko.SFTPClient.from_transport(transport)
    if host == 'testaisgz5.gz-spb.ru' or host == 'testaisgz4.gz-spb.ru':
        folder = '../OOC/IncomingCog/'
    else:
        folder = '../OOC/Incoming/'
    sftp.put(path, f'{folder}{path.split("/")[-1:][0]}')
    print(path.split("/")[-1:][0], 'отправлен на', host)

    if sftp:
        sftp.close()
    if transport:
        transport.close()


def test_folder(host):
    transport = paramiko.Transport(host)
    transport.connect(None, username='root', password=password_sftp)
    sftp = paramiko.SFTPClient.from_transport(transport)
    if host == 'testaisgz5.gz-spb.ru' or host == 'testaisgz4.gz-spb.ru':
        folder = '../OOC/IncomingCog/'
    else:
        folder = '../OOC/Incoming/'

    count = 1

    count_xml = sum([i.count('.xml') for i in sftp.listdir(folder)])
    if count_xml > 0:
        while sum([i.count('.xml') for i in sftp.listdir(folder)]) != 0:
            time.sleep(1)
            print(f'\rИдет отправка пакетов: {count * "|"}', end=' ')
            count += 1
        print(f'\nПакеты отравлены за {count} сек!')
    else:
        print('Пакеты НЕ отравлены!')

    if sftp:
        sftp.close()
    if transport:
        transport.close()


def get_server_address(path: str) -> str:
    """Получить адрес сервера"""
    number = path.split("/")[-1:][0][:3]
    if number == '151':
        return 'testaisgz1.gz-spb.ru'
    elif number == '149':
        return 'testaisgz4.gz-spb.ru'
    elif number == '684':
        return 'testaisgz5.gz-spb.ru'
    elif number == '144':
        return 'testaisgz6.gz-spb.ru'
    else:
        return 'testaisgz3.gz-spb.ru'
