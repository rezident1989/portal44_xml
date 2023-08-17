import copy
from datetime import datetime
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number
import xml.etree.ElementTree as ET


def contract_procedure(outgoing_xml):
    """Исполнение контракта. Публикация"""

    tree = open_xml(outgoing_xml)
    template = open_xml("templates/contractProcedure.xml")

    count_pay_doc = len(tree.findall('.//ns2:execution/ns2:payDoc', ns))
    count_doc_acceptance = len(tree.findall('.//ns2:execution/ns2:docAcceptance', ns))
    count_doc_execution = len(tree.findall('.//ns2:execution/ns2:docExecution', ns))

    if count_pay_doc == 0:
        template.find('.//ns2:executions', ns).remove(template.find(
            './/ns2:execution/ns2:payDoc/..', ns))
    elif count_pay_doc > 1:
        member = copy.deepcopy(template.find('.//ns2:execution/ns2:payDoc/..', ns))
        for i in range(2, count_pay_doc + 1):
            template.find(".//ns2:executions", ns).append(member)

    if count_doc_acceptance == 0:
        template.find('.//ns2:executions', ns).remove(template.find(
            './/ns2:execution/ns2:docAcceptance/..', ns))
    elif count_doc_acceptance > 1:
        member = copy.deepcopy(template.find('.//ns2:execution/ns2:docAcceptance/..', ns))
        for i in range(2, count_doc_acceptance + 1):
            template.find(".//ns2:executions", ns).append(member)

    if count_doc_execution == 0:
        template.find('.//ns2:executions', ns).remove(template.find(
            './/ns2:execution/ns2:docExecution/..', ns))
    elif count_doc_execution > 1:
        member = copy.deepcopy(template.find('.//ns2:execution/ns2:docExecution/..', ns))
        for i in range(2, count_doc_execution + 1):
            template.find(".//ns2:executions", ns).append(member)

    # TODO
    template = ET.ElementTree(template)
    template.write('venv/temp.xml', encoding='utf-8', xml_declaration=True)
    template = open_xml('venv/temp.xml')

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

    for i in range(1, count_pay_doc + 1):
        try:
            template.find(f'.//ns2:execution[{i}]/ns2:payDoc/ns2:sid', ns).text = tree.find(
                f'.//ns2:execution[{i}]/ns2:payDoc/ns2:sid', ns).text
        except AttributeError:
            template.find(f'.//ns2:execution[{i}]/ns2:payDoc/ns2:sid', ns).text = random_number(8)

        template.find(f'.//ns2:execution[{i}]/ns2:payDoc/ns2:externalSid', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:payDoc/ns2:externalSid', ns).text

        template.find(f'.//ns2:execution[{i}]/ns2:payDoc/ns2:documentName', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:payDoc/ns2:documentName', ns).text
        template.find('.//ns2:payDoc/ns2:documentDate', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:payDoc/ns2:documentDate', ns).text
        template.find('.//ns2:payDoc/ns2:documentNum', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:payDoc/ns2:documentNum', ns).text

    for i in range(1, count_doc_acceptance + 1):
        try:
            template.find(f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:sid', ns).text = tree.find(
                f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:sid', ns).text
        except AttributeError:
            template.find(f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:sid', ns).text = random_number(8)

        template.find(f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:externalSid', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:externalSid', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:code', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:code', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:name', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:name', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:documentDate', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:documentDate', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:deliveryAcceptDate', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docAcceptance/ns2:deliveryAcceptDate', ns).text

    for i in range(1, count_doc_execution + 1):
        try:
            template.find(f'.//ns2:execution[{i}]/ns2:docExecution/ns2:sid', ns).text = tree.find(
                f'.//ns2:execution[{i}]/ns2:docExecution/ns2:sid', ns).text
        except AttributeError:
            template.find(f'.//ns2:execution[{i}]/ns2:docExecution/ns2:sid', ns).text = random_number(8)

        template.find(f'.//ns2:execution[{i}]/ns2:docExecution/ns2:externalSid', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docExecution/ns2:externalSid', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docExecution/ns2:code', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docExecution/ns2:code', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docExecution/ns2:name', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docExecution/ns2:name', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docExecution/ns2:documentDate', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docExecution/ns2:documentDate', ns).text
        template.find(f'.//ns2:execution[{i}]/ns2:docExecution/ns2:documentNum', ns).text = tree.find(
            f'.//ns2:execution[{i}]/ns2:docExecution/ns2:documentNum', ns).text

    return template
