from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number
from datetime import datetime

#  Открытый конкурс в электронной форме

purchase_number = None


def eok_notification(outgoing_xml):
    """Извещение о проведении ЭОК20"""

    global purchase_number
    purchase_number = f'23{random_number(17)}'

    tree = open_xml(outgoing_xml)
    template = open_xml("templates/notification/EOK2020/epNotificationEOK2020.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = purchase_number
    template.find('.//ns5:docNumber', ns).text = f'23{random_number(17)}'
    template.find('.//ns5:plannedPublishDate', ns).text = tree.find('.//ns5:plannedPublishDate', ns).text
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    template.find('.//ns5:sid', ns).text = random_number(7)
    template.find('.//ns5:externalSid', ns).text = tree.find('.//ns5:externalSid', ns).text

    return template


def eok_final_protocol(outgoing_xml):
    """Протокол подведения итогов ЭOK20"""

    tree = open_xml(outgoing_xml)
    template = open_xml("templates/notification/EOK2020/epProtocolEOK2020FinalPart.xml")

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = tree.find('.//ns5:externalId', ns).text
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = '2320494564884285722'
    template.find('.//ns5:publishDTInEIS', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:publishDTInETP', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:procedureDT', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns5:signDT', ns).text = datetime.now().strftime("%Y-%m-%d") + '+03:00'

    for el in template.findall('.//ns6:docDate', ns):
        el.text = datetime.now().isoformat()[:-3] + '+03:00'

    return template
