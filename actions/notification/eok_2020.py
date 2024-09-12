import copy
from src.namespace import namespace as ns
from src.system_functions import open_xml, random_number
from datetime import datetime
import xml.etree.ElementTree as ET


#  Открытый конкурс в электронной форме


def eok_sop(outgoing_xml):
    purchase_number = f'24{random_number(17)}'
    doc_number = f'N{random_number(19)}'
    data_now_iso = datetime.now().isoformat()[:-3] + '+03:00'
    data_now = datetime.now().strftime("%Y-%m-%d") + '+03:00'
    sid_stage = random_number(7)
    sid_purchase_object = random_number(7)

    outgoing = open_xml(outgoing_xml)

    #  epNotificationEOK2020
    root = ET.Element(f'{{http://zakupki.gov.ru/oos/export/1}}export')
    root.insert(0, copy.deepcopy(outgoing.find('.//ns1:data', ns)))
    root.find('.//ns1:data', ns).tag = f'{{http://zakupki.gov.ru/oos/export/1}}epNotificationEOK2020'

    try:
        root.find('.//ns4:epNotificationEOK2020/ns5:id', ns).text
    except AttributeError:
        notification = root.find('.//ns4:epNotificationEOK2020', ns)
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

        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}docNumber')
        child.text = doc_number
        common_info.insert(1, child)

        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}publishDTInEIS')
        child.text = data_now_iso
        common_info.insert(3, child)

    for info in root.findall('.//ns6:attachmentInfo', ns):
        try:
            info.find('.//ns6:publishedContentId', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}publishedContentId')
            child.text = 'D94EB5CBDA612D4BE05334548D0AE73F'
            info.insert(0, child)
            child = ET.Element('{http://zakupki.gov.ru/oos/common/1}docDate')
            child.text = data_now_iso
            info.insert(3, child)

    try:
        root.find('.//ns5:collectingInfo/ns5:startDT', ns).text
    except AttributeError:
        start = root.find('.//ns5:collectingInfo', ns)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}startDT')
        child.text = data_now_iso
        start.insert(0, child)

    try:
        root.find('.//ns5:stageInfo/ns5:sid', ns).text
    except AttributeError:
        stage_info = root.find('.//ns5:stageInfo', ns)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}sid')
        child.text = sid_stage
        stage_info.insert(0, child)

    try:
        root.find('.//ns6:purchaseObject/ns6:sid', ns).text
    except AttributeError:
        purchase_object = root.find('.//ns6:purchaseObject', ns)
        child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
        child.text = sid_purchase_object
        purchase_object.insert(0, child)

    # epProtocolEOK2020Final

    root_2 = ET.Element(f'{{http://zakupki.gov.ru/oos/export/1}}export')
    protocol = ET.Element(f'{{http://zakupki.gov.ru/oos/export/1}}epProtocolEOK2020Final')
    protocol.set('schemeVersion', '14.1')
    common_info = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}commonInfo')
    root_2.append(protocol)
    protocol.append(common_info)

    try:
        root_2.find('.//ns4:epProtocolEOK2020Final/ns5:id', ns).text
    except AttributeError:
        protocol = root_2.find('.//ns4:epProtocolEOK2020Final', ns)

        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}id')
        child.text = random_number(8)
        protocol.insert(0, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}externalId')
        child.text = root.find('.//ns5:externalId', ns).text
        protocol.insert(1, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}versionNumber')
        child.text = root.find('.//ns5:versionNumber', ns).text
        protocol.insert(2, child)

    try:
        root_2.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text
    except AttributeError:
        common_info = root_2.find('.//ns5:commonInfo', ns)

        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}purchaseNumber')
        child.text = purchase_number
        common_info.insert(0, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}docNumber')
        child.text = doc_number
        common_info.insert(1, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}publishDTInEIS')
        child.text = data_now_iso
        common_info.insert(2, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}href')
        child.text = 'https://ya.ru'
        common_info.insert(3, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}docNumberExternal')
        child.text = random_number(9)
        common_info.insert(4, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}publishDTInETP')
        child.text = data_now_iso
        common_info.insert(5, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}procedureDT')
        child.text = data_now_iso
        common_info.insert(6, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}signDT')
        child.text = data_now
        common_info.insert(7, child)
        child = ET.Element('{http://zakupki.gov.ru/oos/EPtypes/1}hrefExternal')
        child.text = 'https://ya.ru'
        common_info.insert(8, child)

    template = open_xml("templates/notification/EOK2020/epProtocolEOK2020Final.xml")
    protocol.insert(4, copy.deepcopy(template.find(".//ns5:protocolPublisherInfo", ns)))
    protocol.insert(5, copy.deepcopy(template.find(".//ns5:extPrintFormInfo", ns)))
    protocol.insert(6, copy.deepcopy(template.find(".//ns5:attachmentsInfo", ns)))
    protocol.insert(7, copy.deepcopy(template.find(".//ns5:protocolInfo", ns)))

    for doc in root_2.findall('.//ns6:docDate', ns):
        doc.text = data_now_iso
    for app in root_2.findall('.//ns5:appDT', ns):
        app.text = data_now_iso

    return [root, root_2]
