import copy
import xml.etree.ElementTree as ET
from datetime import datetime

from data.data import Notification
from src.namespace import namespace as ns
from src.system_functions import open_xml, random_number, create_xml, validate_xsd, to_sent_to_sftp, get_server_address

#  Электронный аукцион (или Аукцион в электронной форме)

purchase_number = None


def ef_notification(outgoing_xml):
    """Извещение о проведении ЭА20.
    Новый статус: Подача ценовых предложений"""

    outgoing = open_xml(outgoing_xml)

    class_notification = Notification(purchase_number=f'24{random_number(17)}',
                                      server_address=get_server_address(outgoing_xml))

    root = ET.Element(f'{{http://zakupki.gov.ru/oos/export/1}}export')
    root.insert(0, copy.deepcopy(outgoing.find('.//ns1:data', ns)))
    root.find('.//ns1:data', ns).tag = f'{{http://zakupki.gov.ru/oos/export/1}}epNotificationEF2020'

    notification = root.find('.//ns4:epNotificationEF2020', ns)
    child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}id')
    child.text = random_number(8)
    notification.insert(0, child)

    try:
        root.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text
    except AttributeError:
        common_info = root.find('.//ns5:commonInfo', ns)

        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}purchaseNumber')
        child.text = class_notification.purchase_number
        common_info.insert(0, child)

        child_2 = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}docNumber')
        child_2.text = f'24{random_number(17)}'
        common_info.insert(1, child_2)

        child_3 = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}publishDTInEIS')
        child_3.text = datetime.now().isoformat()[:-3] + '+03:00'
        common_info.insert(3, child_3)

    try:
        root.find('.//ns5:stageInfo/ns5:sid', ns).text
    except AttributeError:
        stage_info = root.find('.//ns5:stageInfo', ns)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}sid')
        child.text = random_number(7)
        stage_info.insert(0, child)

    try:
        root.find('.//ns6:drugPurchaseObjectInfo/ns6:sid', ns).text
    except AttributeError:
        purchase_object = root.find('.//ns6:drugPurchaseObjectInfo', ns)
        child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
        child.text = random_number(7)
        purchase_object.insert(0, child)

    for drug in root.findall('.//ns6:drugInfo', ns):
        try:
            drug.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
            child.text = random_number(8)
            drug.insert(0, child)

    for attachment in root.findall('.//ns6:attachmentInfo', ns):
        try:
            attachment.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}publishedContentId')
            child.text = 'F2975002CB400344E05334548D0A3056'
            attachment.insert(0, child)

            child_2 = ET.Element('{http://zakupki.gov.ru/oos/common/1}docDate')
            child_2.text = datetime.now().isoformat()[:-3] + '+03:00'
            attachment.insert(3, child_2)

    xml = create_xml(root)
    validate_xsd(xml)
    to_sent_to_sftp(xml, class_notification.server_address)

    return class_notification


def ef_submit_offers(outgoing_xml, notification):
    """Протокол подачи ценовых предложений ЭА20.
    Новый статус: Работа комиссии (подведение итогов)"""

    tree = open_xml(outgoing_xml)

    template = open_xml("templates/notification/EF2020/epProtocolEF2020SubmitOffers.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:versionNumber', ns).text = tree.find('.//ns5:versionNumber', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = notification.purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    xml = create_xml(template)
    validate_xsd(xml)
    to_sent_to_sftp(xml, notification.server_address)


def ef_final_protocol(outgoing_xml, notification):
    """Протокол подведения итогов определения поставщика (подрядчика, исполнителя) ЭА20
    Новый статус: Заключение контракта"""

    tree = open_xml(outgoing_xml)

    template = open_xml("templates/notification/EF2020/epProtocolEF2020FinalPart.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = notification.purchase_number
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    template.find('.//ns5:notificationExternalSId', ns).text = tree.find(
        './/ns6:drugPurchaseObjectInfo/ns6:externalSid', ns).text
    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    xml = create_xml(template)
    validate_xsd(xml)
    to_sent_to_sftp(xml, notification.server_address)
