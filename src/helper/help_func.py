import datetime
import re
import xml.etree.ElementTree as ET
from random import randint
from src.helper.schema_xsd import validate_xsd
import os


def open_xml(path):
    """Открывает xml_bag-файл и возвращает его структуру(tree)"""
    tree = ET.ElementTree(file=path)
    return tree


def create_xml(tree):
    """Создает xml-файл"""
    if 'confirmation' in tree.getroot().tag:
        name_file = re.findall(r'[}]\w+', tree.getroot().tag)
    else:
        name_file = re.findall(r'[}]\w+', tree.getroot()[0].tag)
    a = "".join(name_file).replace('}', '')
    path_name = f'incoming/{datetime.datetime.now().strftime("%H.%M_%d.%m.%y_")}{a}.xml'
    tree.write(path_name, encoding='utf-8', xml_declaration=True)
    if 'confirmation' not in path_name:
        validate_xsd(path_name)


def random_number(digits):
    lower = 10 ** (digits - 1)
    upper = 10 ** digits - 1
    return str(randint(lower, upper))


def clear_folder(folder):
    for file in os.listdir(os.path.abspath(f'{folder}')):
        os.remove(os.path.abspath(os.path.join(f'{folder}', file)))
