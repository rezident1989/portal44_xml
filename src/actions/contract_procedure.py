import copy
from datetime import datetime
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number
import xml.etree.ElementTree as ET


def contract_procedure(outgoing_xml):
    """Контракт. Публикация
    template.find('.//ns2:finalStageExecution', ns).text = 'true' - контракт исполниться
    template.find('.//ns2:isEDIBased', ns).text = 'true' - электронное актирование
    """
    tree = open_xml(outgoing_xml)
    template = open_xml('templates/contractProcedure.xml')
    main = template.find(".//ns4:contractProcedure", ns)

    # Добавление в шаблон блока Документа о приемке
    count_pay_doc = len(tree.findall('.//ns2:execution/ns2:payDoc', ns))
    if count_pay_doc == 0:
        template.find('.//ns2:executions', ns).remove(template.find(
            './/ns2:execution/ns2:payDoc/..', ns))
    elif count_pay_doc > 1:
        member = copy.deepcopy(template.find('.//ns2:execution/ns2:payDoc/..', ns))
        for i in range(1, count_pay_doc):
            template.find('.//ns2:executions', ns).append(member)

    # Добавление в шаблон блока Платежный документ
    count_doc_acceptance = len(tree.findall('.//ns2:execution/ns2:docAcceptance', ns))
    if count_doc_acceptance == 0:
        template.find('.//ns2:executions', ns).remove(template.find(
            './/ns2:execution/ns2:docAcceptance/..', ns))
    elif count_doc_acceptance > 1:
        member = copy.deepcopy(template.find('.//ns2:execution/ns2:docAcceptance/..', ns))
        for i in range(1, count_doc_acceptance):
            template.find('.//ns2:executions', ns).append(member)

    # Добавление в шаблон блока Документа об исполнении контракта
    count_doc_execution = len(tree.findall('.//ns2:execution/ns2:docExecution', ns))
    if count_doc_execution == 0:
        template.find('.//ns2:executions', ns).remove(template.find(
            './/ns2:execution/ns2:docExecution/..', ns))
    elif count_doc_execution > 1:
        member = copy.deepcopy(template.find('.//ns2:execution/ns2:docExecution/..', ns))
        for i in range(1, count_doc_execution):
            template.find('.//ns2:executions', ns).append(member)

    # Добавление в шаблон блока Информация о неустойках (штрафах, пениях)
    count_penalties = len(tree.findall('.//ns2:penalties', ns))
    if count_penalties > 0:
        list_penalties = tree.findall('.//ns2:penalties', ns)
        for i, penalties in enumerate(list_penalties):
            main.insert(6 + i, copy.deepcopy(penalties))

    # Копирование блока contractProcedure/executionObligationGuarantee
    try:
        a = tree.find('.//ns2:executionObligationGuarantee', ns).text
        if a is None:
            raise
        main.remove(template.find(".//ns2:executions", ns))
        main.insert(5, copy.deepcopy(tree.find(".//ns2:executionObligationGuarantee", ns)))
    except AttributeError:
        # Заполнение блока contractProcedure/execution/stage
        member = template.find('.//ns2:stage', ns)
        try:
            member.find('.//ns2:sid', ns).text = tree.find('.//ns2:stage/ns2:sid', ns).text
        except AttributeError:
            member.remove(member.find('.//ns2:sid', ns))
        try:
            member.find('.//ns2:externalSid', ns).text = tree.find('.//ns2:stage/ns2:externalSid', ns).text
        except AttributeError:
            member.remove(member.find('.//ns2:externalSid', ns))
        try:
            member.find('.//ns2:endDate', ns).text = tree.find('.//ns2:stage/ns2:endDate', ns).text
        except AttributeError:
            member.remove(member.find('.//ns2:endDate', ns))
        template.find('.//ns2:finalStageExecution', ns).text = tree.find('.//ns2:finalStageExecution', ns).text

    # # TODO Создать временный xml-файл
    # template = ET.ElementTree(template)
    # template.write('venv/temp.xml', encoding='utf-8', xml_declaration=True)
    # template = open_xml('venv/temp.xml')

    # Заполнение блока contractProcedure
    template.find('.//ns2:id', ns).text = random_number(8)
    template.find('.//ns2:regNum', ns).text = tree.find('.//ns2:regNum', ns).text
    template.find('.//ns2:publishDate', ns).text = datetime.now().isoformat()[:-3] + '+03:00'

    # Заполнение блока contractProcedure/execution/stage/execution/payDoc
    for i1, tag_temp in enumerate(template.findall('.//ns2:execution/ns2:payDoc/..', ns)):
        for i2, tag_three in enumerate(tree.findall('.//ns2:execution/ns2:payDoc/..', ns)):
            if i1 == i2:
                try:
                    tag_temp.find('.//ns2:sid', ns).text = tree.find('.//ns2:sid', ns).text
                except AttributeError:
                    tag_temp.find('.//ns2:sid', ns).text = random_number(8)
                tag_temp.find('.//ns2:externalSid', ns).text = tag_three.find('.//ns2:externalSid', ns).text
                tag_temp.find('.//ns2:documentName', ns).text = tag_three.find('.//ns2:documentName', ns).text
                tag_temp.find('.//ns2:documentDate', ns).text = tag_three.find('.//ns2:documentDate', ns).text
                tag_temp.find('.//ns2:documentNum', ns).text = tag_three.find('.//ns2:documentNum', ns).text

    # Заполнение блока contractProcedure/execution/stage/execution/docAcceptance
    for i1, tag_temp in enumerate(template.findall('.//ns2:execution/ns2:docAcceptance/..', ns)):
        for i2, tag_three in enumerate(tree.findall('.//ns2:execution/ns2:docAcceptance/..', ns)):
            if i1 == i2:
                try:
                    tag_temp.find('./ns2:sid', ns).text = tag_three.find('./ns2:sid', ns).text
                except AttributeError:
                    tag_temp.find('.//ns2:sid', ns).text = random_number(8)
                tag_temp.find('.//ns2:externalSid', ns).text = tag_three.find('.//ns2:externalSid', ns).text
                tag_temp.find('.//ns2:code', ns).text = tag_three.find('.//ns2:code', ns).text
                tag_temp.find('.//ns2:name', ns).text = tag_three.find('.//ns2:name', ns).text
                tag_temp.find('.//ns2:documentDate', ns).text = tag_three.find('.//ns2:documentDate', ns).text
                tag_temp.find('.//ns2:deliveryAcceptDate', ns).text = tag_three.find(
                    './/ns2:deliveryAcceptDate', ns).text

    # Заполнение блока contractProcedure/execution/stage/execution/docExecution
    for i1, tag_temp in enumerate(template.findall('.//ns2:execution/ns2:docExecution/..', ns)):
        for i2, tag_three in enumerate(tree.findall('.//ns2:execution/ns2:docExecution/..', ns)):
            if i1 == i2:
                try:
                    tag_temp.find('.//ns2:sid', ns).text = tag_three.find('.//ns2:sid', ns).text
                except AttributeError:
                    tag_temp.find('.//ns2:sid', ns).text = random_number(8)
                tag_temp.find('.//ns2:externalSid', ns).text = tag_three.find('.//ns2:externalSid', ns).text
                tag_temp.find('.//ns2:code', ns).text = tag_three.find('.//ns2:code', ns).text
                tag_temp.find('.//ns2:name', ns).text = tag_three.find('.//ns2:name', ns).text
                tag_temp.find('.//ns2:documentDate', ns).text = tag_three.find('.//ns2:documentDate', ns).text
                tag_temp.find('.//ns2:documentNum', ns).text = tag_three.find('.//ns2:documentNum', ns).text

    return template
