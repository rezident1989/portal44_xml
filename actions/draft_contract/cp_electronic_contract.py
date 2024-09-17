import copy
import xml.etree.ElementTree as ET

from src.namespace import namespace as ns
from src.system_functions import open_xml, random_number, create_xml, to_sent_to_sftp, get_server_address


def cp_electronic_contract(outgoing_xml, send=True):
    """Электронный контракт"""

    outgoing = open_xml(outgoing_xml)

    root = copy.deepcopy(outgoing.find('.//ns1:data', ns))
    root.tag = f'{{http://zakupki.gov.ru/oos/export/1}}cpElectronicContract'

    for i, stage in enumerate(root.findall('.//ns7:stageInfo', ns)):
        try:
            stage.find('.//ns7:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/CPtypes/1}sid')
            child.text = random_number(8)
            stage.insert(0, child)

    for i, purchase_object in enumerate(root.findall('.//ns7:productInfo', ns)):
        try:
            purchase_object.find('.//ns7:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/CPtypes/1}sid')
            child.text = random_number(8)
            purchase_object.insert(0, child)

    for i, drug_purchase_object in enumerate(root.findall('.//ns7:drugProductInfo', ns)):
        try:
            drug_purchase_object.find('.//ns7:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/CPtypes/1}sid')
            child.text = random_number(8)
            drug_purchase_object.insert(0, child)

    xml = create_xml(root)

    if send:
        to_sent_to_sftp(xml, f'{get_server_address(outgoing_xml)}')
