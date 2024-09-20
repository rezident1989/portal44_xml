import os
import random
import sys
import time
from datetime import datetime
from xml.etree.ElementTree import ElementTree, Element

import paramiko
from lxml import etree

from hidden.sftp_connect import username_sftp, password_sftp


def open_xml(path: str) -> Element:
    """Открыть xml"""
    return ElementTree(file=path).getroot()


def get_type_xml(path: str) -> str:
    """Получить название пакета xml"""
    return open_xml(path).tag.split('}')[1]


def create_xml(elem: Element) -> str:
    """Создать xml файлы и вернуть список их путей """
    path_xml_list = []
    date_time = datetime.now().strftime("%H.%M.%S___%d.%m.%y___")

    if os.path.isdir('incoming') is not True:
        os.makedirs('incoming')

    if 'export' == elem.tag.split('}')[1]:
        name_file = elem[0].tag.split('}')[1]
    else:
        name_file = elem.tag.split('}')[1]

    name = "".join(name_file).replace('}', '')

    if name_file == 'cpElectronicContract':
        path_name = os.path.relpath(os.path.join('incoming', '10_CpElectronicContract.xml'))
    else:
        path_name = os.path.relpath(os.path.join('incoming', f'{date_time}{name}.xml'))

    path_xml_list.append(path_name)

    ElementTree(elem).write(path_name, encoding='utf-8', xml_declaration=True)

    return path_name


def random_number(number: int) -> str:
    """Сгенерировать случайное число, number количество цифр в числе"""
    if number < 1:
        return 'Ошибка. Необходимо целое число, больше нуля'
    return str(random.randint(10 ** (number - 1), 10 ** number - 1))


def clear_folder(folder: str) -> None:
    """Очистить папку"""
    if os.path.isdir(folder) is not True:
        os.makedirs(folder)
    for file in os.listdir(os.path.abspath(f'{folder}')):
        os.remove(os.path.abspath(os.path.join(f'{folder}', file)))


def remove_file(file: str, folder: str, send=True) -> None:
    """Переместить в папку"""
    if send:
        if os.path.isdir(folder) is not True:
            os.makedirs(folder)
        a = file.split('\\')[-1:][0]
        os.replace(file, f'{folder}\\{a}')


def to_sent_to_sftp(path: str, host: str) -> None:
    """Отравить xml на сервер"""
    transport = paramiko.Transport(host)
    transport.connect(None, username=username_sftp, password=password_sftp)
    sftp = paramiko.SFTPClient.from_transport(transport)

    if 'CpElectronicContract' in path.split('\\')[-1:][0]:
        folder = '/castle/www/gpospb/cometp/data/CpElectronicContractsTest/'
    elif host == 'testaisgz4.gz-spb.ru':
        folder = '/OOC/IncomingCog/'
    else:
        folder = '../OOC/Incoming/'
    a = path.split('\\')[-1:][0]
    sftp.put(path, f'{folder}{a}')
    print(path.split('\\')[-1:][0], 'отправлен на', host)

    if sftp:
        sftp.close()
    if transport:
        transport.close()
    test_folder(host)


def test_folder(host: str) -> None:
    """Проверить есть ли xml в очереди на обработку"""
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
            print(f'\rЖдем, пока XML обработает КРОН: {count * "|"}', end=' ')
            count += 1
        print(f'\rXML обработан за {count} сек!')
    else:
        print('XML отправлен на сервер, без очереди')

    if sftp:
        sftp.close()
    if transport:
        transport.close()


def get_server_address(path: str) -> str:
    """Получить адрес сервера"""
    number = path.split('\\')[-1:][0][:5]
    if number == '17188':
        return 'testaisgz1.gz-spb.ru'
    elif number == '16894':
        return 'testaisgz6.gz-spb.ru'
    elif number == '68435':
        return 'testaisgz5.gz-spb.ru'
    else:
        print('Непонятно куда кидать пакет((')
        sys.exit(1)


def validate_xsd(path: str, version='14_2') -> None:
    """Валидация схемы"""
    if 'outgoing' in path or 'CpElectronicContract' in path:
        schema_path = f'src\\schemes\\{version}\\fcsIntegration.xsd'
    else:
        schema_path = f'src\\schemes\\{version}\\fcsExport.xsd'

    path_xsd = etree.parse(schema_path)
    schema = etree.XMLSchema(path_xsd)

    # Загрузка xml
    xml = etree.parse(path)

    file_name = path.split('\\')[1]
    schema_number = schema_path.split('\\')[2]

    # Проверка
    if not schema.validate(xml):
        print(schema.error_log)
        sys.exit(1)
    else:
        print(f'{file_name} соответствует схеме {schema_number}')


def get_path_xml() -> str:
    """Проверка папки 'outgoing'"""
    if os.path.isdir('outgoing') is not True:
        os.makedirs('outgoing')

    a = len(os.listdir('outgoing'))

    if a == 1 and os.listdir('outgoing')[0].endswith('.xml'):
        return os.path.relpath(os.path.join('outgoing', os.listdir('outgoing')[0]))
    elif a == 1 and not os.listdir('outgoing')[0].endswith('.xml'):
        print(f'В папке "outgoing" нет XML-файла! Необходимо добавить 1 XML-файл, остальные файлы удалить!')
    elif a == 0:
        print(f'Папка "outgoing" пустая! Необходимо добавить 1 XML-файл!')
    else:
        print(f'В папке "outgoing" больше 1 файла ({a})! Необходимо оставить 1 XML-файл, остальные файлы удалить!')
    sys.exit(1)


def current_date_and_time_iso() -> str:
    return f'{datetime.now().isoformat()[:-3]}+03:00'


def current_date_and_time() -> str:
    return f'{datetime.now().strftime("%Y-%m-%d")}+03:00'


def current_year() -> str:
    return f'{datetime.now().year}'
