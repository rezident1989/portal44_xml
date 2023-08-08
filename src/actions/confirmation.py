from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml, random_number
import xml.etree.ElementTree as ET
import secrets


def confirmation(outgoing_xml):
    """Подтверждение"""

    tree = open_xml(outgoing_xml).getroot()
    template = open_xml('templates/confirmation.xml').getroot()

    template.find('.//ns1:id', ns).text = secrets.token_hex(18)
    template.find('.//ns2:loadId', ns).text = random_number(8)
    template.find('.//ns2:refId', ns).text = tree.find('.//ns1:id', ns).text

    create_xml(ET.ElementTree(template))
