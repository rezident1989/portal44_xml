import copy
import xml.etree.ElementTree as ET
from random import randint
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml
from datetime import datetime


def contract(outgoing_xml):
    """
    """

    tree = open_xml(outgoing_xml).getroot()
    template = ET.ElementTree(file="templates/contract.xml").getroot()

    remove = False

    template.find('.//ns2:id', ns).text = template.find('.//ns2:id', ns).text[:-4] + str(randint(1000, 9999))
    template.find('.//ns2:externalId', ns).text = tree.find('.//ns2:externalId', ns).text
    template.find('.//ns2:placementDate', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    member = template.find(".//ns4:contract", ns)
    member.remove(template.find(".//ns2:foundation", ns))
    member.insert(5, copy.deepcopy(tree.find(".//ns2:foundation", ns)))
    member = template.find(".//ns4:contract", ns)
    member.remove(template.find(".//ns2:customer", ns))
    member.insert(6, copy.deepcopy(tree.find(".//ns2:customer", ns)))
    member = template.find(".//ns4:contract", ns)
    member.remove(template.find(".//ns2:placer", ns))
    member.insert(7, copy.deepcopy(tree.find(".//ns2:placer", ns)))
    member = template.find(".//ns4:contract", ns)
    member.remove(template.find(".//ns2:finances", ns))
    member.insert(8, copy.deepcopy(tree.find(".//ns2:finances", ns)))

    try:
        template.find('.//ns2:protocolDate', ns).text = tree.find('.//ns2:protocolDate', ns).text
    except AttributeError:
        remove = True

    template.find('.//ns2:documentCode', ns).text = template.find('.//ns2:documentCode', ns).text[:-4] + str(
        randint(1000, 9999))
    template.find('.//ns2:signDate', ns).text = tree.find('.//ns2:signDate', ns).text

    try:
        template.find('.//ns4:contract/ns2:regNum', ns).text = tree.findall(
            './/ns1:data/ns2:regNum', ns).text
    except AttributeError:
        template.find('.//ns4:contract/ns2:regNum', ns).text = template.find(
            './/ns4:contract/ns2:regNum', ns).text[:-4] + str(randint(1000, 9999))

    template.find('.//ns2:number', ns).text = tree.find('.//ns2:number', ns).text
    template.find('.//ns2:contractSubject', ns).text = tree.find('.//ns2:contractSubject', ns).text
    member = template.find(".//ns4:contract", ns)
    member.remove(template.find(".//ns2:priceInfo", ns))
    member.insert(17, copy.deepcopy(tree.find(".//ns2:priceInfo", ns)))
    member = template.find(".//ns4:contract", ns)
    member.remove(template.find(".//ns2:executionPeriod", ns))
    member.insert(18, copy.deepcopy(tree.find(".//ns2:executionPeriod", ns)))
    member = template.find(".//ns4:contract", ns)
    member.remove(template.find(".//ns2:products", ns))
    member.insert(19, copy.deepcopy(tree.find(".//ns2:products", ns)))
    template.find('.//ns2:executionPeriod', ns).text = tree.find('.//ns2:executionPeriod', ns).text

    for el in template.findall('.//ns2:docRegNumber', ns):
        el.text = template.findall('.//ns2:docRegNumber', ns)[0].text[:-4] + str(randint(1000, 9999))

    if remove:
        member.remove(template.find(".//ns2:protocolDate", ns))

    create_xml(ET.ElementTree(template))
