import datetime
import re
import xml.etree.ElementTree as ET
from src.helper.schema_xsd import validate_xsd


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
