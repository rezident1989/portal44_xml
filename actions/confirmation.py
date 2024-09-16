from secrets import token_hex
from xml.etree.ElementTree import Element, SubElement

from src.system_functions import open_xml, random_number, current_date_and_time_iso, get_server_address, create_xml, \
    to_sent_to_sftp
from src.namespace import namespace as ns


def confirmation(path_xml: str, send=True):
    """Подтверждение"""

    server_address = get_server_address(path_xml)

    our_xml = open_xml(path_xml)

    root = Element(f'{{http://zakupki.gov.ru/oos/integration/1}}confirmation')

    elem_1 = SubElement(root, f'{{http://zakupki.gov.ru/oos/integration/1}}index')
    elem_2 = SubElement(root, f'{{http://zakupki.gov.ru/oos/integration/1}}data')
    elem_2.attrib = our_xml.find('.//ns1:data', ns).attrib
    SubElement(elem_1, f'{{http://zakupki.gov.ru/oos/integration/1}}id').text = token_hex(18)
    SubElement(elem_1, f'{{http://zakupki.gov.ru/oos/integration/1}}sender').text = 'OOC'
    SubElement(elem_1, f'{{http://zakupki.gov.ru/oos/integration/1}}createDateTime'). \
        text = current_date_and_time_iso()
    SubElement(elem_1, f'{{http://zakupki.gov.ru/oos/integration/1}}objectType').text = 'CT'
    SubElement(elem_1, f'{{http://zakupki.gov.ru/oos/integration/1}}objectId')
    SubElement(elem_1, f'{{http://zakupki.gov.ru/oos/integration/1}}signature', {'type': 'CAdES-BES'})
    SubElement(elem_1, f'{{http://zakupki.gov.ru/oos/integration/1}}mode').text = 'PROD'
    SubElement(elem_2, f'{{http://zakupki.gov.ru/oos/types/1}}loadId').text = random_number(8)
    SubElement(elem_2, f'{{http://zakupki.gov.ru/oos/types/1}}result').text = 'success'  # failure
    SubElement(elem_2, f'{{http://zakupki.gov.ru/oos/types/1}}refId'). \
        text = our_xml.find('.//ns1:id', ns).text

    xml = create_xml(root)
    # validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, server_address)
