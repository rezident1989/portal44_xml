from datetime import datetime
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number


def contract_procedure(outgoing_xml):
    """Исполнение контракта. Публикация"""

    tree = open_xml(outgoing_xml)
    template = open_xml("templates/contractProcedure.xml")

    template.find('.//ns2:id', ns).text = random_number(8)
    template.find('.//ns2:regNum', ns).text = tree.find('.//ns2:regNum', ns).text
    template.find('.//ns2:publishDate', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    template.find('.//ns2:finalStageExecution', ns).text = tree.find('.//ns2:finalStageExecution', ns).text
    template.find('.//ns2:finalStageExecution', ns).text = 'false'
    template.find('.//ns2:isEDIBased', ns).text = 'false'

    try:
        template.find('.//ns2:stage/ns2:sid', ns).text = tree.find('.//ns2:stage/ns2:sid', ns).text
    except AttributeError:
        template.find('.//ns2:stage/ns2:sid', ns).text = random_number(8)
    template.find('.//ns2:stage/ns2:externalSid', ns).text = tree.find(
        './/ns2:stage/ns2:externalSid', ns).text

    try:
        template.find('.//ns2:execution/ns2:payDoc/ns2:sid', ns).text = tree.find(
            './/ns2:execution/ns2:payDoc/ns2:sid', ns).text
    except AttributeError:
        template.find('.//ns2:execution/ns2:payDoc/ns2:sid', ns).text = random_number(8)

    template.find('.//ns2:execution/ns2:payDoc/ns2:externalSid', ns).text = tree.find(
        './/ns2:execution/ns2:payDoc/ns2:externalSid', ns).text

    template.find('.//ns2:execution/ns2:payDoc/ns2:documentName', ns).text = tree.find(
        './/ns2:execution/ns2:payDoc/ns2:documentName', ns).text
    template.find('.//ns2:payDoc/ns2:documentDate', ns).text = tree.find(
        './/ns2:execution/ns2:payDoc/ns2:documentDate', ns).text
    template.find('.//ns2:payDoc/ns2:documentNum', ns).text = tree.find(
        './/ns2:execution/ns2:payDoc/ns2:documentNum', ns).text

    try:
        template.find('.//ns2:execution/ns2:docAcceptance/ns2:sid', ns).text = tree.find(
            './/ns2:execution/ns2:docAcceptance/ns2:sid', ns).text
    except AttributeError:
        template.find('.//ns2:execution/ns2:docAcceptance/ns2:sid', ns).text = random_number(8)

    template.find('.//ns2:execution/ns2:docAcceptance/ns2:externalSid', ns).text = tree.find(
        './/ns2:execution/ns2:docAcceptance/ns2:externalSid', ns).text
    template.find('.//ns2:execution/ns2:docAcceptance/ns2:code', ns).text = tree.find(
        './/ns2:execution/ns2:docAcceptance/ns2:code', ns).text
    template.find('.//ns2:execution/ns2:docAcceptance/ns2:name', ns).text = tree.find(
        './/ns2:execution/ns2:docAcceptance/ns2:name', ns).text
    template.find('.//ns2:execution/ns2:docAcceptance/ns2:documentDate', ns).text = tree.find(
        './/ns2:execution/ns2:docAcceptance/ns2:documentDate', ns).text
    template.find('.//ns2:execution/ns2:docAcceptance/ns2:deliveryAcceptDate', ns).text = tree.find(
        './/ns2:execution/ns2:docAcceptance/ns2:deliveryAcceptDate', ns).text

    try:
        template.find('.//ns2:execution/ns2:docExecution/ns2:sid', ns).text = tree.find(
            './/ns2:execution/ns2:docExecution/ns2:sid', ns).text
    except AttributeError:
        template.find('.//ns2:execution/ns2:docExecution/ns2:sid', ns).text = random_number(8)

    template.find('.//ns2:execution/ns2:docExecution/ns2:externalSid', ns).text = tree.find(
        './/ns2:execution/ns2:docExecution/ns2:externalSid', ns).text
    template.find('.//ns2:execution/ns2:docExecution/ns2:code', ns).text = tree.find(
        './/ns2:execution/ns2:docExecution/ns2:code', ns).text
    template.find('.//ns2:execution/ns2:docExecution/ns2:name', ns).text = tree.find(
        './/ns2:execution/ns2:docExecution/ns2:name', ns).text
    template.find('.//ns2:execution/ns2:docExecution/ns2:documentDate', ns).text = tree.find(
        './/ns2:execution/ns2:docExecution/ns2:documentDate', ns).text
    template.find('.//ns2:execution/ns2:docExecution/ns2:documentNum', ns).text = tree.find(
        './/ns2:execution/ns2:docExecution/ns2:documentNum', ns).text

    return template
