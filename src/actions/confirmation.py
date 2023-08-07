from random import randint
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml
import xml.etree.ElementTree as ET


def confirmation(outgoing_xml):
    """
    Подтверждение
    id - Глобальный идентификатор информационного пакета. от ЕИС
    loadId - Номер текущей сессии. от ЕИС
    refId - Глобальный идентификатор информационного пакета. от ИМЦ
    """

    tree = open_xml(outgoing_xml).getroot()
    template = open_xml('templates/confirmation.xml').getroot()

    template.find('.//ns1:id', ns).text = template.find('.//ns1:id', ns).text[:-4] + str(randint(1000, 9999))
    template.find('.//ns2:loadId', ns).text = str(randint(10000000, 99999999))
    template.find('.//ns2:refId', ns).text = tree.find('.//ns1:id', ns).text

    create_xml(ET.ElementTree(template))
