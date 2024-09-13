import copy
from src.namespace import namespace as ns
from src.system_functions import open_xml, random_number
from datetime import datetime
import xml.etree.ElementTree as ET

#  Электронный аукцион (или Аукцион в электронной форме)

purchase_number = None


def ef_notification(outgoing_xml):
    """Извещение о проведении ЭА20.
    Новый статус: Подача ценовых предложений"""

    global purchase_number
    purchase_number = f'24{random_number(17)}'

    outgoing = open_xml(outgoing_xml)

    #  epNotificationEOK2020
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
        child.text = purchase_number
        common_info.insert(0, child)

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

    # try:
    #     root.find('.//ns6:purchaseObject/ns6:sid', ns).text
    # except AttributeError:
    #     purchase_object = root.find('.//ns6:purchaseObject', ns)
    #     child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
    #     child.text = random_number(7)
    #     purchase_object.insert(0, child)

    return [root]


def ef_submit_offers(outgoing_xml):
    """Протокол подачи ценовых предложений ЭА20.
    Новый статус: Работа комиссии (подведение итогов)"""

    tree = open_xml(outgoing_xml)
    template = open_xml("templates/notification/EF2020/epProtocolEF2020SubmitOffers.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:versionNumber', ns).text = tree.find('.//ns5:versionNumber', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    return [template]


def ef_final_protocol(outgoing_xml):
    """Протокол подведения итогов определения поставщика (подрядчика, исполнителя) ЭА20
    Новый статус: Заключение контракта"""

    tree = open_xml(outgoing_xml)
    template = open_xml("templates/notification/EF2020/epProtocolEF2020FinalPart.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    template.find('.//ns5:notificationExternalSId', ns).text = tree.find(
        './/ns6:drugPurchaseObjectInfo/ns6:externalSid', ns).text
    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    return [template]

# purchase_number = f'24{random_number(17)}'
#
# tree = open_xml(outgoing_xml)
# template = open_xml("templates/notification/EF2020/epNotificationEF.xml")
#
# template.find('.//ns5:id', ns).text = random_number(8)
# template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
# template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
# template.find('.//ns5:docNumber', ns).text = f'24{random_number(17)}'
# template.find('.//ns5:plannedPublishDate', ns).text = tree.find('.//ns5:plannedPublishDate', ns).text
# template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
# template.find('.//ns5:purchaseObjectInfo', ns).text = tree.find('.//ns5:purchaseObjectInfo', ns).text
#
# for el in template.findall('.//ns6:docDate', ns):
#     el.text = datetime.now().isoformat()[:-3] + '+03:00'
#
# template.find('.//ns5:endDT', ns).text = tree.find('.//ns5:endDT', ns).text
# template.find('.//ns5:summarizingDate', ns).text = tree.find('.//ns5:summarizingDate', ns).text
# template.find('.//ns5:sid', ns).text = random_number(7)
# template.find('.//ns5:externalSid', ns).text = tree.find('.//ns5:externalSid', ns).text
#
# number_position = 0
# main = template.find(".//ns4:epNotificationEF2020", ns)
#
# #  Писал для совместной закупки, непонятно нужно или нет
# try:
#     path = 'ns5:notificationInfo'
#     main.remove(main.find(path, ns))
#     main.insert(number_position + 20, copy.deepcopy(tree.find('.//ns5:notificationInfo', ns)))
#     for position in template.findall(f'.//ns5:DrugPurchaseObjectsInfo//ns6:purchaseObject', ns):
#         try:
#             position.find('.//ns6:sid', ns).text
#         except AttributeError:
#             child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
#             child.text = random_number(8)
#             position.insert(0, child)
# except TypeError:
#     number_position -= 1
