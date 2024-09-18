from copy import deepcopy
from xml.etree.ElementTree import Element

from src.namespace import namespace as ns
from src.system_functions import open_xml, random_number, current_date_and_time_iso, current_year, get_server_address, \
    create_xml, validate_xsd, to_sent_to_sftp


def tender_plan_2020(path_xml: str, send=True):
    """Добавление или редактирование позиции (особой позиции) в опубликованный в ЕИС план-график"""

    server_address = get_server_address(path_xml)

    our_xml = open_xml(path_xml)

    root = Element(f'{{http://zakupki.gov.ru/oos/export/1}}export')
    root.insert(0, deepcopy(our_xml.find('.//ns1:data', ns)))
    root.find('.//ns1:data', ns).tag = f'{{http://zakupki.gov.ru/oos/export/1}}tenderPlan2020'
    main_elem = root.find('.//ns4:tenderPlan2020', ns)

    try:
        main_elem.find('./ns3:id', ns).text  # id
    except AttributeError:
        child = Element('{http://zakupki.gov.ru/oos/TPtypes/1}id')
        child.text = random_number(8)
        main_elem.insert(0, child)

    try:
        main_elem.find('./ns3:planNumber', ns).text  # planNumber
    except AttributeError:
        child = Element('{http://zakupki.gov.ru/oos/TPtypes/1}planNumber')
        child.text = current_year() + str(random_number(14))
        main_elem.insert(2, child)

    elem = main_elem.find('./ns3:commonInfo', ns)
    child = Element('{http://zakupki.gov.ru/oos/TPtypes/1}confirmDate')  # confirmDate
    child.text = current_date_and_time_iso()
    elem.insert(2, child)

    elem = main_elem.find('./ns3:commonInfo', ns)
    child = Element('{http://zakupki.gov.ru/oos/TPtypes/1}publishDate')  # publishDate
    child.text = current_date_and_time_iso()
    elem.insert(3, child)

    positions = main_elem.findall('.//ns3:position/ns3:commonInfo', ns)
    special_positions = main_elem.findall('.//ns3:specialPurchasePosition', ns)

    for position in positions:
        try:
            position.find('.//ns3:positionNumber', ns).text
        except AttributeError:
            child = Element('{http://zakupki.gov.ru/oos/TPtypes/1}positionNumber')  # positionNumber
            child.text = f'{current_year()}{random_number(20)}'
            position.insert(0, child)

    for position in special_positions:
        try:
            position.find('.//ns3:positionNumber', ns).text
        except AttributeError:
            child = Element('{http://zakupki.gov.ru/oos/TPtypes/1}positionNumber')  # positionNumber
            child.text = f'{current_year()}{random_number(20)}'
            position.insert(1, child)

    xml = create_xml(root)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, server_address)
