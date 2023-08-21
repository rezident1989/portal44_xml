import copy
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number
from datetime import datetime


def contract(outgoing_xml):
    """Контракт. Публикация"""

    tree = open_xml(outgoing_xml)
    template = open_xml("templates/contract.xml")

    remove = False
    member = template.find(".//ns4:contract", ns)

    template.find('.//ns2:id', ns).text = random_number(8)
    template.find('.//ns2:externalId', ns).text = tree.find('.//ns2:externalId', ns).text
    template.find('.//ns2:placementDate', ns).text = datetime.now().isoformat()[:-3] + '+03:00'

    member.remove(template.find(".//ns2:foundation", ns))
    member.insert(5, copy.deepcopy(tree.find(".//ns2:foundation", ns)))
    member.remove(template.find(".//ns2:customer", ns))
    member.insert(7, copy.deepcopy(tree.find(".//ns2:customer", ns)))
    member.remove(template.find(".//ns2:placer", ns))
    member.insert(8, copy.deepcopy(tree.find(".//ns2:placer", ns)))
    member.remove(template.find(".//ns2:finances", ns))
    member.insert(9, copy.deepcopy(tree.find(".//ns2:finances", ns)))
    try:
        template.find('.//ns2:protocolDate', ns).text = tree.find('.//ns2:protocolDate', ns).text
    except AttributeError:
        remove = True

    template.find('.//ns2:documentCode', ns).text = random_number(6)
    template.find('.//ns2:signDate', ns).text = tree.find('.//ns2:signDate', ns).text
    try:
        template.find('.//ns4:contract/ns2:regNum', ns).text = tree.find('.//ns1:data/ns2:regNum', ns).text
    except AttributeError:
        template.find('.//ns4:contract/ns2:regNum', ns).text = random_number(19)
    template.find('.//ns2:number', ns).text = tree.find('.//ns2:number', ns).text
    template.find('.//ns2:contractSubject', ns).text = tree.find('.//ns2:contractSubject', ns).text
    member.remove(template.find(".//ns2:priceInfo", ns))
    member.insert(19, copy.deepcopy(tree.find(".//ns2:priceInfo", ns)))
    member.remove(template.find(".//ns2:executionPeriod", ns))
    member.insert(21, copy.deepcopy(tree.find(".//ns2:executionPeriod", ns)))
    member.remove(template.find(".//ns2:products", ns))
    member.insert(23, copy.deepcopy(tree.find(".//ns2:products", ns)))

    for el in template.findall('.//ns2:docRegNumber', ns):
        el.text = random_number(19)

    if len(tree.findall('.//ns2:supplierAccountDetails/ns6:externalSid', ns)) > 0:
        template.find('.//ns2:supplierAccountDetails/ns6:externalSid', ns).text = tree.find(
            './/ns2:supplierAccountDetails/ns6:externalSid', ns).text

        try:
            template.find('.//ns2:supplierAccountDetails/ns6:sid', ns).text = tree.find(
                './/ns2:supplierAccountDetails/ns6:sid', ns).text
        except AttributeError:
            template.find('.//ns2:supplierAccountDetails/ns6:sid', ns).text = random_number(8)

    if remove:
        member.remove(template.find(".//ns2:protocolDate", ns))

    return template
