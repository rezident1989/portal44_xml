import copy
import xml.etree.ElementTree as ET
from datetime import datetime

from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml, random_number


def contract_procedure(outgoing_xml):
    """Исполнение контракта. Публикация"""

    tree = open_xml(outgoing_xml).getroot()
    template = ET.ElementTree(file="templates/contractProcedure.xml").getroot()

    remove = False
    member = template.find(".//ns3:contract", ns)

    template.find('.//ns2:id', ns).text = random_number(9)
    template.find('.//ns4:contractProcedure/ns2:regNum', ns).text = tree.find('.//ns1:data/ns2:regNum', ns).text
    template.find('.//ns2:publishDate', ns).text = datetime.now().isoformat()[:-3] + '+03:00'

    try:
        template.find('.//ns2:protocolDate', ns).text = tree.find('.//ns2:protocolDate', ns).text
    except AttributeError:
        template.find('.//ns2:stage/ns2:sid', ns).text = random_number(8)
    template.find('.//ns2:stage/ns2:externalSid', ns).text = tree.find('.//ns2:stage/ns2:externalSid', ns).text
    template.find('.//ns2:finalStageExecution', ns).text = tree.find('.//ns2:finalStageExecution', ns).text

    try:
        template.find('.//ns2:payDoc/ns2:sid', ns).text = tree.find('.//ns2:payDoc/ns2:sid', ns).text
    except AttributeError:
        template.find('.//ns2:payDoc/ns2:sid', ns).text = random_number(8)
    template.find('.//ns2:payDoc/ns2:externalSid', ns).text = tree.find('.//ns2:payDoc/ns2:sid', ns).text

    try:
        template.find('.//ns2:docAcceptance/ns2:sid', ns).text = tree.find('.//ns2:docAcceptance/ns2:sid', ns).text
    except AttributeError:
        template.find('.//ns2:docAcceptance/ns2:sid', ns).text = random_number(8)
    template.find('.//ns2:docAcceptance/ns2:externalSid', ns).text = tree.find('.//ns2:docAcceptance/ns2:sid', ns).text

    try:
        template.find('.//ns2:docExecution/ns2:sid', ns).text = tree.find('.//ns2:docExecution/ns2:sid', ns).text
    except AttributeError:
        template.find('.//ns2:docExecution/ns2:sid', ns).text = random_number(8)
    template.find('.//ns2:docExecution/ns2:externalSid', ns).text = tree.find('.//ns2:docExecution/ns2:sid', ns).text

    template.find('.//ns2:isEDIBased', ns).text = True

    create_xml(ET.ElementTree(template), outgoing_xml.split("/")[-1:][0][:2])