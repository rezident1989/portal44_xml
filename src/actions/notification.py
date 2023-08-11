import xml.etree.ElementTree as ET
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml, random_number
from datetime import datetime

purchase_number = None


def ep_notification_ef_2020(outgoing_xml):
    """Подача ценовых предложений"""
    global purchase_number
    purchase_number = random_number(19)

    tree = open_xml(outgoing_xml).getroot()
    template = ET.ElementTree(file="templates/epNotificationEF.xml").getroot()

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:docNumber', ns).text = random_number(19)
    template.find('.//ns5:plannedPublishDate', ns).text = tree.find('.//ns5:plannedPublishDate', ns).text
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:purchaseObjectInfo', ns).text = tree.find('.//ns5:purchaseObjectInfo', ns).text

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    template.find('.//ns5:endDT', ns).text = tree.find('.//ns5:endDT', ns).text
    template.find('.//ns5:summarizingDate', ns).text = tree.find('.//ns5:summarizingDate', ns).text
    template.find('.//ns5:sid', ns).text = random_number(7)
    template.find('.//ns5:externalSid', ns).text = tree.find('.//ns5:externalSid', ns).text

    create_xml(ET.ElementTree(template), outgoing_xml.split("/")[-1:][0][:2])


def ep_protocol_ef_2020_submit_offers(outgoing_xml):
    """Работа комиссии (подведение итогов)"""

    tree = open_xml(outgoing_xml).getroot()
    template = ET.ElementTree(file="templates/epProtocolEF2020SubmitOffers.xml").getroot()

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:versionNumber', ns).text = tree.find('.//ns5:versionNumber', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    create_xml(ET.ElementTree(template), outgoing_xml.split("/")[-1:][0][:2])


def ep_protocol_ef_2020_final(outgoing_xml):
    """Заключение контракта"""

    tree = open_xml(outgoing_xml).getroot()
    template = ET.ElementTree(file="templates/epProtocolEF2020Final.xml").getroot()

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    create_xml(ET.ElementTree(template), outgoing_xml.split("/")[-1:][0][:2])
