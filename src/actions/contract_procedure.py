import xml.etree.ElementTree as ET
from random import randint
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml


def contract_procedure(outgoing_xml):
    """Информация об исполнении (расторжении) контракта"""
