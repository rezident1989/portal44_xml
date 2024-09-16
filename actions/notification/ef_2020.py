import copy
import xml.etree.ElementTree as ET
from datetime import datetime

from data.data import Notification
from src.namespace import namespace as ns
from src.system_functions import (open_xml, random_number, create_xml, validate_xsd, to_sent_to_sftp,
                                  get_server_address, current_year, current_date_and_time)

#  Электронный аукцион (или Аукцион в электронной форме)

purchase_number = None


def ef_notification(outgoing_xml, send=True):
    """Извещение о проведении ЭА20.
    Новый статус: Подача ценовых предложений"""

    outgoing = open_xml(outgoing_xml)

    notification = Notification()

    notification.server_address = f'{get_server_address(outgoing_xml)}'
    notification.schema_version = outgoing.find('.//ns1:data', ns).attrib
    notification.id = random_number(8)
    notification.version_number = outgoing.find('.//ns5:versionNumber', ns).text
    notification.external_id = outgoing.find('.//ns5:externalId', ns).text
    notification.purchase_number = f'{current_year()[2:]}{random_number(17)}'
    notification.doc_number = f'{current_year()[2:]}{random_number(17)}'
    notification.publish_in_eis = datetime.now().isoformat()[:-3] + '+03:00'
    notification.stages = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns5:stageInfo', ns))))
    notification.purchase_objects = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns6:purchaseObject', ns))))
    notification.drug_purchase_objects = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns6:drugPurchaseObjectInfo', ns))))
    notification.drugs = tuple(
        random_number(8) for _ in range(len(outgoing.findall('.//ns6:drugInfo', ns))))

    root = ET.Element(f'{{http://zakupki.gov.ru/oos/export/1}}export')
    root.insert(0, copy.deepcopy(outgoing.find('.//ns1:data', ns)))
    root.find('.//ns1:data', ns).tag = f'{{http://zakupki.gov.ru/oos/export/1}}epNotificationEF2020'

    name_xml = root.find('.//ns4:epNotificationEF2020', ns)
    child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}id')
    child.text = notification.id
    name_xml.insert(0, child)

    try:
        root.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text
    except AttributeError:
        common_info = root.find('.//ns5:commonInfo', ns)

        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}purchaseNumber')
        child.text = notification.purchase_number
        common_info.insert(0, child)

        child_2 = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}docNumber')
        child_2.text = notification.doc_number
        common_info.insert(1, child_2)

        child_3 = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}publishDTInEIS')
        child_3.text = notification.publish_in_eis
        common_info.insert(3, child_3)

    for i, stage in enumerate(root.findall('.//ns5:stageInfo', ns)):
        try:
            stage.find('.//ns5:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}sid')
            child.text = notification.stages[i]
            stage.insert(0, child)

    for i, purchase_object in enumerate(root.findall('.//ns6:purchaseObject', ns)):
        try:
            purchase_object.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
            child.text = notification.purchase_objects[i]
            purchase_object.insert(0, child)

    for i, drug_purchase_object in enumerate(root.findall('.//ns6:drugPurchaseObjectInfo', ns)):
        try:
            drug_purchase_object.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
            child.text = notification.drug_purchase_objects[i]
            drug_purchase_object.insert(0, child)

    for i, drug in enumerate(root.findall('.//ns6:drugInfo', ns)):
        try:
            drug.find('.//ns6:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
            child.text = notification.drugs[i]
            drug.insert(0, child)

    for attachment in root.findall('.//ns6:attachmentInfo', ns):
        # TODO Подумать нужно ли добавлять в экз. класса
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
    if send:
        to_sent_to_sftp(xml, notification.server_address)

    return notification


def ef_submit_offers(notification, send=True):
    """Протокол подачи ценовых предложений ЭА20.
    Новый статус: Работа комиссии (подведение итогов)"""

    template = open_xml("templates/notification/EF2020/epProtocolEF2020SubmitOffers_altova.xml")

    template.find('.//ns4:epProtocolEF2020SubmitOffers', ns).attrib = notification.schema_version

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = notification.external_id
    template.find('.//ns5:versionNumber', ns).text = notification.version_number
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = notification.purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = notification.publish_in_eis
    template.find('.//ns5:procedureDT', ns).text = notification.publish_in_eis
    template.find('.//ns5:signDT', ns).text = current_date_and_time()

    xml = create_xml(template)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, notification.server_address)


def ef_final_part_protocol(notification, send=True):
    """Протокол подведения итогов определения поставщика (подрядчика, исполнителя) ЭА20
    Новый статус: Заключение контракта"""

    template = open_xml("templates/notification/EF2020/epProtocolEF2020FinalPart_altova.xml")

    template.find('.//ns4:epProtocolEF2020FinalPart', ns).attrib = notification.schema_version

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = notification.external_id
    template.find('.//ns5:versionNumber', ns).text = notification.version_number
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = notification.purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = notification.publish_in_eis
    template.find('.//ns5:procedureDT', ns).text = notification.publish_in_eis
    template.find('.//ns5:signDT', ns).text = current_date_and_time()

    try:
        template.find(
            './/ns5:productInfo/ns5:notificationExternalSId', ns).text = notification.purchase_objects[0]
    except (AttributeError, IndexError):
        a = template.find('.//ns5:drugProposalsInfo/..', ns)
        b = template.find('.//ns5:drugProposalsInfo', ns)
        a.remove(b)

    try:
        template.find('.//ns5:drugPurchaseObjectInfo/ns5:notificationExternalSId', ns).text = (
            notification.drug_purchase_objects)[0]
    except (AttributeError, IndexError):
        a = template.find('.//ns5:notDrugProposalsInfo/..', ns)
        b = template.find('.//ns5:notDrugProposalsInfo', ns)
        a.remove(b)

    xml = create_xml(template)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, notification.server_address)
