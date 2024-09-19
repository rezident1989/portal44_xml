import xml.etree.ElementTree as ET

from src.namespace import namespace as ns
from src.system_functions import open_xml, random_number, create_xml, to_sent_to_sftp, get_server_address, validate_xsd


def cp_electronic_contract(outgoing_xml, send=True):
    """Электронный контракт"""

    root = open_xml(outgoing_xml)

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
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, f'{get_server_address(outgoing_xml)}')


def cp_electronic_contract_eis(data, send=True):
    """Электронный контракт"""

    root = open_xml("templates/draft_contract/10_CpElectronicContract.xml")

    for i, stage in enumerate(root.findall('.//ns7:stageInfo', ns)):
        stage.find('.//ns7:sid', ns).text = random_number(8)

    for i, purchase_object in enumerate(root.findall('.//ns7:productInfo', ns)):
        purchase_object.find('.//ns7:sid', ns).text = random_number(8)

    for i, drug_purchase_object in enumerate(root.findall('.//ns7:drugProductInfo', ns)):
        drug_purchase_object.find('.//ns7:sid', ns).text = random_number(8)

    root.find('.//ns7:purchaseNumber', ns).text = data.purchase_number
    root.find('.//ns7:purchaseCode', ns).text = data.purchase_code
    root.find('.//ns7:protocolObjectSid', ns).text = data.purchase_protocol_sid[0]
    root.find('.//ns7:purchaseObjectSid', ns).text = data.purchase_objects_sid[0]
    root.find('.//ns7:purchaseObjectExternalSid', ns).text = data.purchase_objects_external_sid[0]

    xml = create_xml(root)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, f'{data.server_address}')
