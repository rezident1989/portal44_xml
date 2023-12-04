import copy
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number
from datetime import datetime
import xml.etree.ElementTree as ET


def contract(outgoing_xml):
    """Контракт. Публикация"""

    tree = open_xml(outgoing_xml)
    template = open_xml("src/templates/contract.xml")

    main = template.find(".//ns4:contract", ns)

    # Заполнение блока contractProcedure
    main.find('.//ns2:id', ns).text = random_number(8)
    main.find('.//ns2:externalId', ns).text = tree.find('.//ns2:externalId', ns).text
    main.find('.//ns2:placementDate', ns).text = datetime.now().isoformat()[:-3] + '+03:00'
    main.find('.//ns2:publishDate', ns).text = tree.find('.//ns2:publishDate', ns).text
    main.find('.//ns2:documentCode', ns).text = random_number(6)
    main.find('.//ns2:signDate', ns).text = tree.find('.//ns2:signDate', ns).text
    template.find('.//ns2:number', ns).text = tree.find('.//ns2:number', ns).text
    template.find('.//ns2:contractSubject', ns).text = tree.find('.//ns2:contractSubject', ns).text

    # Полная замена блоков
    main.remove(template.find(".//ns2:foundation", ns))
    main.insert(5, copy.deepcopy(tree.find(".//ns2:foundation", ns)))
    main.remove(template.find(".//ns2:customer", ns))
    main.insert(7, copy.deepcopy(tree.find(".//ns2:customer", ns)))
    main.remove(template.find(".//ns2:placer", ns))
    main.insert(8, copy.deepcopy(tree.find(".//ns2:placer", ns)))
    main.remove(template.find(".//ns2:finances", ns))
    main.insert(9, copy.deepcopy(tree.find(".//ns2:finances", ns)))
    main.remove(template.find(".//ns2:priceInfo", ns))
    main.insert(19, copy.deepcopy(tree.find(".//ns2:priceInfo", ns)))
    main.remove(template.find(".//ns2:executionPeriod", ns))
    main.insert(21, copy.deepcopy(tree.find(".//ns2:executionPeriod", ns)))
    main.remove(template.find(".//ns2:products", ns))
    main.insert(23, copy.deepcopy(tree.find(".//ns2:products", ns)))
    main.remove(template.find(".//ns2:suppliersInfo", ns))
    main.insert(24, copy.deepcopy(tree.find(".//ns2:suppliersInfo", ns)))

    try:
        template.find('.//ns4:contract/ns2:regNum', ns).text = tree.find('.//ns1:data/ns2:regNum', ns).text
    except AttributeError:
        template.find('.//ns4:contract/ns2:regNum', ns).text = random_number(19)

    try:
        main.find('.//ns2:versionNumber', ns).text = tree.find('.//ns2:versionNumber', ns).text
    except AttributeError:
        main.find('.//ns2:versionNumber', ns).text = '0'

    # Добавить тег sid в блоки contract/executionPeriod/stages
    for stages in template.findall('.//ns2:executionPeriod/ns2:stages', ns):
        try:
            stages.find('.//ns2:sid', ns).text
        except AttributeError:

            child = ET.Element('{http://zakupki.gov.ru/oos/types/1}sid')
            child.text = random_number(8)
            stages.insert(0, child)

    # Добавить тег sid в блоки contract/suppliersInfo/supplierInfo/supplierAccountsDetails/supplierAccountDetails
    # Необязательный блок
    if len(tree.findall('.//ns2:supplierAccountDetails', ns)) > 0:
        for account in template.findall('.//ns2:supplierAccountDetails', ns):
            try:
                account.find('.//ns6:sid', ns).text
            except AttributeError:
                child = ET.Element('{http://zakupki.gov.ru/oos/common/1}sid')
                child.text = random_number(8)
                account.insert(0, child)

    # Заполнение блока contractProcedure с возможным удалением
    # Необязательный блок
    try:
        template.find('.//ns2:protocolDate', ns).text = tree.find('.//ns2:protocolDate', ns).text
    except AttributeError:
        main.remove(template.find(".//ns2:protocolDate", ns))

    return template
