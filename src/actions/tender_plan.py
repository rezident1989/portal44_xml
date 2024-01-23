import copy
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number
import xml.etree.ElementTree as ET


def tender_plan_2020(outgoing_xml):
    """Добавление позиции (особой позиции) в опубликованный в ЕИС план-график"""

    template = open_xml('src/templates/tenderPlan2020.xml')
    tree = open_xml(outgoing_xml)

    main = template.find(".//ns4:tenderPlan2020", ns)
    number_position = 4

    # Заполнить простые теги блока tenderPlan2020
    main.attrib['schemeVersion'] = tree.find('.//ns1:data', ns).attrib.get('schemeVersion')
    template.find('.//ns3:id', ns).text = random_number(8)
    template.find('.//ns3:externalId', ns).text = tree.find('.//ns3:externalId', ns).text

    try:
        template.find('.//ns3:planNumber', ns).text = tree.find('.//ns3:planNumber', ns).text
    except AttributeError:
        template.find('.//ns3:planNumber', ns).text = '2024' + str(random_number(14))

    template.find('.//ns3:versionNumber', ns).text = tree.find('.//ns3:versionNumber', ns).text

    # Заполнить блок commonInfo
    confirm_contact_info = copy.deepcopy(main.find('.//ns3:confirmContactInfo', ns))

    path = './/ns3:commonInfo'
    main.remove(template.find(path, ns))
    main.insert(number_position, copy.deepcopy(tree.find(path, ns)))

    confirm_date = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}confirmDate')
    confirm_date.text = tree.find('.//ns1:createDateTime', ns).text
    template.find(path, ns).insert(2, confirm_date)

    publish_date = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}publishDate')
    publish_date.text = tree.find('.//ns1:createDateTime', ns).text
    template.find(path, ns).insert(3, publish_date)

    main.find(path, ns).insert(6, confirm_contact_info)

    # Заполнить необязательный блок positions
    try:
        path = './/ns3:positions'
        main.remove(template.find(path, ns))
        main.insert(number_position + 1, copy.deepcopy(tree.find(path, ns)))
        for position in template.findall(f'{path}/ns3:position/ns3:commonInfo', ns):
            try:
                position.find('.//ns3:positionNumber', ns).text
            except AttributeError:
                child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}positionNumber')
                child.text = f'2024{random_number(20)}'
                position.insert(0, child)
    except TypeError:
        number_position = number_position - 1

    # Заполнить необязательный блок specialPurchasePositions
    try:
        path = './/ns3:specialPurchasePositions'
        main.remove(template.find(path, ns))
        main.insert(number_position + 2, copy.deepcopy(tree.find(path, ns)))
        for special_position in template.findall(f'{path}/ns3:specialPurchasePosition', ns):
            try:
                special_position.find('.//ns3:positionNumber', ns).text
            except AttributeError:
                child = ET.Element('{http://zakupki.gov.ru/oos/TPtypes/1}positionNumber')
                child.text = f'2024{random_number(20)}'
                special_position.insert(0, child)
    except TypeError:
        pass

    return template
