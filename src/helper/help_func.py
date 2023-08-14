import datetime
import re
import xml.etree.ElementTree as ET
from random import randint
from src.helper.schema_xsd import validate_xsd
import os
import paramiko
from password import password_sftp


def open_xml(path):
    """Открывает xml_bag-файл и возвращает его структуру(tree)"""
    tree = ET.ElementTree(file=path)
    return tree


def create_xml(tree, server):
    """Создает xml-файл"""
    if 'confirmation' in tree.getroot().tag:
        name_file = re.findall(r'[}]\w+', tree.getroot().tag)
    else:
        name_file = re.findall(r'[}]\w+', tree.getroot()[0].tag)

    date_time = datetime.datetime.now().strftime("%H.%M_%d.%m.%y_")
    name = "".join(name_file).replace('}', '')
    path_name = f'incoming/{date_time}{name}.xml'
    tree.write(path_name, encoding='utf-8', xml_declaration=True)
    if 'confirmation' not in path_name:
        validate_xsd(path_name)

    to_sent_to_sftp(path_name, server)


def to_sent_to_sftp(path, server):
    # Open a transport
    if server == '15':
        host = 'testaisgz1.gz-spb.ru'
    elif server == '14':
        host = 'testaisgz6.gz-spb.ru'
    elif server == '68':
        host = 'testaisgz5.gz-spb.ru'
    else:
        host = 'testaisgz3.gz-spb.ru'
    transport = paramiko.Transport(host)

    transport.connect(None, username='root', password=password_sftp)
    sftp = paramiko.SFTPClient.from_transport(transport)

    # Go!
    if server == '68':
        sftp.put(path, f'../OOC/IncomingCog/{path.split("/")[-1:][0]}')
    else:
        sftp.put(path, f'../OOC/Incoming/{path.split("/")[-1:][0]}')
    print(path.split("/")[-1:][0], 'отправлен на', host)
    # Close a transport
    if sftp:
        sftp.close()
    if transport:
        transport.close()


def random_number(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    return str(randint(lower, upper))


def clear_folder(folder):
    for file in os.listdir(os.path.abspath(f'{folder}')):
        os.remove(os.path.abspath(os.path.join(f'{folder}', file)))
