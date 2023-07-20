import datetime
import re
import xml.etree.ElementTree as ET


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
    tree.write(
        f'incoming/{datetime.datetime.now().strftime("%H.%M_%d.%m.%y_")}{a}.xml', encoding='utf-8',
        xml_declaration=True)
