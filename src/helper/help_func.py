import datetime
import time
import random
import os
import sys
import xml.etree.ElementTree as ET

import paramiko
from lxml import etree

from hidden.sftp_connect import username_sftp, password_sftp


def open_xml(path: str) -> ET.Element:
    """Открывает xml"""
    return ET.ElementTree(file=path).getroot()


def random_number(digits: int) -> str:
    """Генерация случайное число"""
    if digits < 1:
        return 'Ошибка. Необходимо целое число, больше нуля'
    return str(random.randint(10 ** (digits - 1), 10 ** digits - 1))


def clear_folder(folder: str) -> None:
    """Очистить папку"""
    if os.path.isdir(folder) is not True:
        os.makedirs(folder)
    for file in os.listdir(os.path.abspath(f'{folder}')):
        os.remove(os.path.abspath(os.path.join(f'{folder}', file)))


def remove_file(file: str, folder: str) -> None:
    """Переместить в папку"""
    if os.path.isdir(folder) is not True:
        os.makedirs(folder)
    a = file.split('\\')[-1:][0]
    os.replace(file, f'{folder}\\{a}')


def get_type_xml(path: str) -> str:
    """Получить название пакета xml"""
    return open_xml(path).tag.split('}')[1]


def create_xml(tree: ET.Element) -> str:
    """Создает xml"""
    if 'export' == tree.tag.split('}')[1]:
        name_file = tree[0].tag.split('}')[1]
    else:
        name_file = 'confirmation'
    date_time = datetime.datetime.now().strftime("%H.%M.%S___%d.%m.%y___")
    name = "".join(name_file).replace('}', '')
    if os.path.isdir('incoming') is not True:
        os.makedirs('incoming')
    path_name = os.path.relpath(os.path.join('incoming', f'{date_time}{name}.xml'))
    tree = ET.ElementTree(tree)
    tree.write(path_name, encoding='utf-8', xml_declaration=True)

    return path_name


def to_sent_to_sftp(path, host):
    transport = paramiko.Transport(host)
    transport.connect(None, username=username_sftp, password=password_sftp)
    sftp = paramiko.SFTPClient.from_transport(transport)
    if host == 'testaisgz4.gz-spb.ru':
        folder = '../OOC/IncomingCog/'
    else:
        folder = '../OOC/Incoming/'
    a = path.split('\\')[-1:][0]
    sftp.put(path, f'{folder}{a}')
    print(path.split('\\')[-1:][0], 'отправлен на', host)

    if sftp:
        sftp.close()
    if transport:
        transport.close()


def test_folder(host):
    transport = paramiko.Transport(host)
    transport.connect(None, username=username_sftp, password=password_sftp)
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
    number = path.split('\\')[-1:][0][:5]
    if number == '16767':
        return 'testaisgz1.gz-spb.ru'
    elif number == '16893':
        return 'testaisgz6.gz-spb.ru'
    elif number == '68435':
        return 'testaisgz5.gz-spb.ru'
    else:
        return 'testaisgz3.gz-spb.ru'


def validate_xsd(path, version='14_1'):
    # Загрузка xsd схемы
    if 'outgoing' in path:
        schema_path = f'src\\schemes\\{version}\\fcsIntegration.xsd'
    else:
        schema_path = f'src\\schemes\\{version}\\fcsExport.xsd'

    path_xsd = etree.parse(schema_path)
    schema = etree.XMLSchema(path_xsd)

    # Загрузка xml
    xml = etree.parse(path)

    a = path.split('\\')[1]
    b = schema_path.split('\\')[2]

    # Проверка
    if not schema.validate(xml):
        print(schema.error_log)
        sys.exit(1)
    else:
        print(f'{a} соответствует схеме {b}')


def get_path_xml() -> str:

    if os.path.isdir('outgoing') is not True:
        os.makedirs('outgoing')

    a = len(os.listdir('outgoing'))

    if a == 1 and os.listdir('outgoing')[0].endswith('.xml'):
        return os.path.relpath(os.path.join('outgoing', os.listdir('outgoing')[0]))
    elif a == 1 and not os.listdir('outgoing')[0].endswith('.xml'):
        print(f'В папке "outgoing" нет XML-файла! Необходимо добавить 1 XML-файл, остальные файлы удалить!')
        sys.exit(1)
    elif a == 0:
        print(f'Папка "outgoing" пустая! Необходимо добавить 1 XML-файл!')
        sys.exit(1)
    else:
        print(f'В папке "outgoing" больше 1 файла ({a})! Необходимо оставить 1 XML-файл, остальные файлы удалить!')
        sys.exit(1)
