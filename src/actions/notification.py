import copy
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number
from datetime import datetime
import xml.etree.ElementTree as ET

purchase_number = None


def ep_notification_ef_2020(outgoing_xml):
    """Подача ценовых предложений"""
    global purchase_number
    purchase_number = f'23{random_number(17)}'

    tree = open_xml(outgoing_xml)
    template = open_xml("src/templates/epNotificationEF.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:docNumber', ns).text = f'23{random_number(17)}'
    template.find('.//ns5:plannedPublishDate', ns).text = tree.find('.//ns5:plannedPublishDate', ns).text
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:purchaseObjectInfo', ns).text = tree.find('.//ns5:purchaseObjectInfo', ns).text

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    template.find('.//ns5:endDT', ns).text = tree.find('.//ns5:endDT', ns).text
    template.find('.//ns5:summarizingDate', ns).text = tree.find('.//ns5:summarizingDate', ns).text
    template.find('.//ns5:sid', ns).text = random_number(7)
    template.find('.//ns5:externalSid', ns).text = tree.find('.//ns5:externalSid', ns).text

    number_position = 0
    main = template.find(".//ns4:epNotificationEF2020", ns)

    try:
        path = 'ns5:notificationInfo'
        main.remove(main.find(path, ns))
        main.insert(number_position + 20, copy.deepcopy(tree.find('.//ns5:notificationInfo', ns)))
        for position in template.findall(f'.//ns5:notDrugPurchaseObjectsInfo//ns6:purchaseObject', ns):
            try:
                position.find('.//ns6:sid', ns).text
            except AttributeError:
                child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
                child.text = random_number(8)
                position.insert(0, child)
    except TypeError:
        number_position -= 1

    return template


def ep_protocol_ef_2020_submit_offers(outgoing_xml):
    """Работа комиссии (подведение итогов)"""

    tree = open_xml(outgoing_xml)
    template = open_xml("src/templates/epProtocolEF2020SubmitOffers.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:versionNumber', ns).text = tree.find('.//ns5:versionNumber', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    return template


def ep_protocol_ef_2020_final(outgoing_xml):
    """Заключение контракта"""

    tree = open_xml(outgoing_xml)
    template = open_xml("src/templates/epProtocolEF2020Final.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    return template


def ep_notification_ezt_2020(outgoing_xml):
    """Подача ценовых предложений"""
    global purchase_number
    purchase_number = f'23{random_number(17)}'

    tree = open_xml(outgoing_xml)
    template = open_xml("src/templates/epNotificationEZT2020.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:docNumber', ns).text = f'23{random_number(17)}'
    template.find('.//ns5:plannedPublishDate', ns).text = tree.find('.//ns5:plannedPublishDate', ns).text
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    # template.find('.//ns5:purchaseObjectInfo', ns).text = tree.find('.//ns5:purchaseObjectInfo', ns).text

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    # template.find('.//ns5:endDT', ns).text = tree.find('.//ns5:endDT', ns).text
    # template.find('.//ns5:summarizingDate', ns).text = tree.find('.//ns5:summarizingDate', ns).text
    template.find('.//ns5:sid', ns).text = random_number(7)
    template.find('.//ns5:externalSid', ns).text = tree.find('.//ns5:externalSid', ns).text

    return template


def ep_protocol_ezt_2020_submit_offers(outgoing_xml):
    """Работа комиссии (подведение итогов)"""

    tree = open_xml(outgoing_xml)
    template = open_xml("src/templates/epProtocolEF2020SubmitOffers.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:versionNumber', ns).text = tree.find('.//ns5:versionNumber', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    return template


def ep_protocol_ezt_2020_final(outgoing_xml):
    """Заключение контракта"""

    tree = open_xml(outgoing_xml)
    template = open_xml("src/templates/epProtocolEZT2020Final.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    return template
