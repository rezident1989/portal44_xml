import xml.etree.ElementTree as ET
from copy import deepcopy

from src.helper.help_func import open_xml, random_number, current_date_and_time_iso, current_year
from src.helper.namespace import namespace as ns


def tender_plan_2020(doc_xml):
    """Добавление или редактирование позиции (особой позиции) в опубликованный в ЕИС план-график"""

    our_xml = open_xml(doc_xml)

    root = ET.Element(f'{{http://zakupki.gov.ru/oos/export/1}}export')  # tenderPlan2020
    root.insert(0, deepcopy(our_xml.find('.//ns1:data', ns)))
    root.find('.//ns1:data', ns).tag = f'{{http://zakupki.gov.ru/oos/export/1}}tenderPlan2020'
    main_elem = root.find('.//ns4:tenderPlan2020', ns)

    try:
        main_elem.find('./ns3:id', ns).text  # id
    except AttributeError:
        child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}id')
        child.text = random_number(8)
        main_elem.insert(0, child)

    try:
        main_elem.find('./ns3:planNumber', ns).text  # planNumber
    except AttributeError:
        child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}planNumber')
        child.text = current_year() + str(random_number(14))
        main_elem.insert(2, child)

    elem = main_elem.find('./ns3:commonInfo', ns)
    child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}confirmDate')  # confirmDate
    child.text = current_date_and_time_iso()
    elem.insert(2, child)

    elem = main_elem.find('./ns3:commonInfo', ns)
    child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}publishDate')  # publishDate
    child.text = current_date_and_time_iso()
    elem.insert(3, child)

    positions = main_elem.findall('.//ns3:position/ns3:commonInfo', ns)
    special_positions = main_elem.findall('.//ns3:specialPurchasePosition', ns)

    for position in positions:
        try:
            position.find('.//ns3:positionNumber', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}positionNumber')  # positionNumber
            child.text = f'{current_year()}{random_number(20)}'
            position.insert(0, child)

    for position in special_positions:
        try:
            position.find('.//ns3:positionNumber', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}positionNumber')  # positionNumber
            child.text = f'{current_year()}{random_number(20)}'
            position.insert(1, child)

    return [root]
