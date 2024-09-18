import copy
import xml.etree.ElementTree as ET
from datetime import datetime

from src.namespace import namespace as ns
from src.system_functions import open_xml, random_number, get_server_address, create_xml, validate_xsd, to_sent_to_sftp


def contract_procedure(outgoing_xml, send=True):
    """Исполнение контракта
    finalStageExecution = 'true' - контракт исполниться
    isEDIBased = 'true' - электронное актирование
    """

    b = get_server_address(outgoing_xml)

    tree = open_xml(outgoing_xml)
    template = open_xml('templates/contract/contractProcedure.xml')
    main = template.find(".//ns4:contractProcedure", ns)

    receipt_documents_template = main.find('.//ns2:receiptDocuments', ns)

    # Полная замена блоков
    main.remove(template.find(".//ns2:executions", ns))
    main.insert(5, copy.deepcopy(tree.find(".//ns2:executions", ns)))

    # Основа
    template.find('.//ns2:id', ns).text = random_number(8)
    template.find('.//ns2:regNum', ns).text = tree.find('.//ns2:regNum', ns).text
    template.find('.//ns2:publishDate', ns).text = datetime.now().isoformat()[:-3] + '+03:00'

    # Платежный документ, Документ о приемке, Документ об исполнении
    a = (main.findall('.//ns2:executions/ns2:execution/ns2:payDoc', ns) +
         main.findall('.//ns2:executions/ns2:execution/ns2:docAcceptance', ns) +
         main.findall('.//ns2:executions/ns2:execution/ns2:docExecution', ns))

    for account in a:
        try:
            account.find('./ns2:sid', ns).text
        except AttributeError:
            child = ET.Element('{http://zakupki.gov.ru/oos/types/1}sid')
            child.text = random_number(8)
            account.insert(0, child)
        try:
            account.remove(account.find('.//ns2:receiptDocuments', ns))
            account.insert(100, receipt_documents_template)
        except (AttributeError, TypeError):
            pass

    # Добавление в шаблон блока Информация о неустойках (штрафах, пениях)
    count_penalties = len(tree.findall('.//ns2:penalties', ns))
    if count_penalties > 0:
        list_penalties = tree.findall('.//ns2:penalties', ns)
        for i, penalties in enumerate(list_penalties):
            main.insert(6 + i, copy.deepcopy(penalties))

    # Добавление в шаблон блока Информация об отсрочках оплаты неустоек
    count_penalties_2 = len(tree.findall('.//ns2:delayWriteOffPenalties', ns))
    if count_penalties_2 > 0:
        list_penalties_2 = tree.findall('.//ns2:delayWriteOffPenalties', ns)
        for i, penalties_2 in enumerate(list_penalties_2):
            main.insert(6 + i, copy.deepcopy(penalties_2))

    xml = create_xml(main)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, b)
