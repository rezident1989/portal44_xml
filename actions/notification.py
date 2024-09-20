import copy
import xml.etree.ElementTree as ET
from datetime import datetime

from data.data import Purchase
from src.namespace import namespace as ns
from src.system_functions import (open_xml, random_number, create_xml, validate_xsd, to_sent_to_sftp,
                                  get_server_address, current_year)


def notification(outgoing_xml, type_notification, send=True):
    """
    epNotificationEF2020
    epClosedInvitationEZakA2020
    Переход в статус: Подача ценовых предложений
    """

    outgoing = open_xml(outgoing_xml)

    data = Purchase()

    data.server_address = f'{get_server_address(outgoing_xml)}'
    data.schema_version = outgoing.find('.//ns1:data', ns).attrib
    data.id = random_number(8)
    data.version_number = outgoing.find('.//ns5:versionNumber', ns).text
    data.external_id = outgoing.find('.//ns5:externalId', ns).text
    data.purchase_number = f'{current_year()[2:]}{random_number(17)}'
    data.doc_number = f'{current_year()[2:]}{random_number(17)}'
    data.publish_in_eis = datetime.now().isoformat()[:-3] + '+03:00'
    data.stages = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns5:stageInfo', ns))))
    data.purchase_objects_sid = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns6:purchaseObject', ns))))
    data.drug_purchase_objects_sid = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns6:drugPurchaseObjectInfo', ns))))
    data.drugs = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns6:drugInfo', ns))))

    root = ET.Element(f'{{http://zakupki.gov.ru/oos/export/1}}export')
    root.insert(0, copy.deepcopy(outgoing.find('.//ns1:data', ns)))
    root.find('.//ns1:data', ns).tag = f'{{http://zakupki.gov.ru/oos/export/1}}{type_notification}'

    name_xml = root.find(f'.//ns4:{type_notification}', ns)
    child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}id')
    child.text = data.id
    name_xml.insert(0, child)

    try:
        root.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text
    except AttributeError:
        common_info = root.find('.//ns5:commonInfo', ns)

        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}purchaseNumber')
        child.text = data.purchase_number
        common_info.insert(0, child)

        child_2 = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}docNumber')
        child_2.text = data.doc_number
        common_info.insert(1, child_2)

        child_3 = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}publishDTInEIS')
        child_3.text = data.publish_in_eis
        common_info.insert(3, child_3)

    for i, stage in enumerate(root.findall('.//ns5:stageInfo', ns)):
        try:
            stage.find('.//ns5:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}sid')
            child.text = data.stages[i]
            stage.insert(0, child)

    for i, purchase_object in enumerate(root.findall('.//ns6:purchaseObject', ns)):
        try:
            purchase_object.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
            child.text = data.purchase_objects_sid[i]
            purchase_object.insert(0, child)

    for i, drug_purchase_object in enumerate(root.findall('.//ns6:drugPurchaseObjectInfo', ns)):
        try:
            drug_purchase_object.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
            child.text = data.drug_purchase_objects_sid[i]
            drug_purchase_object.insert(0, child)

    for i, drug in enumerate(root.findall('.//ns6:drugInfo', ns)):
        try:
            drug.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
            child.text = data.drugs[i]
            drug.insert(0, child)

    for attachment in root.findall('.//ns6:attachmentInfo', ns):
        # TODO Подумать нужно ли добавлять в экз. класса
        try:
            attachment.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}publishedContentId')
            child.text = 'F2975002CB400344E05334548D0A3056'
            attachment.insert(0, child)

            # child_2 = ET.Element('{http://zakupki.gov.ru/oos/common/1}docDate')
            # child_2.text = datetime.now().isoformat()[:-3] + '+03:00'
            # attachment.insert(2, child_2)

    # TODO Подумать как оптимизировать
    data.purchase_objects_external_sid = tuple(
        el.text for el in root.findall('.//ns6:purchaseObject/ns6:externalSid', ns))

    data.drug_external_sid = tuple(
        el.text for el in root.findall('.//ns6:drugPurchaseObjectInfo/ns6:externalSid', ns))

    data.purchase_code = root.find('.//ns5:purchaseCode', ns).text
    data.placing_way_cod = root.find('.//ns5:placingWay/ns8:code', ns).text

    xml = create_xml(root)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, data.server_address)

    return data
