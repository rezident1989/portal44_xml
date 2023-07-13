import copy
import xml.etree.ElementTree as ET
from random import randint
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml


def tender_plan_2020(outgoing_xml):
    """
    План-график закупок с 01.01.2020
    id - Идентификатор ревизии плана-графика закупок в ЕИС. От ЕИС
    externalId - Внешний идентификатор документа
    planNumber - Реестровый номер плана-графика закупок в ЕИС
    versionNumber - Номер версии плана-графика закупок
    confirmDate - Дата утверждения версии плана-графика закупок

    commonInfo/specialPurchasePosition - обычная/специальная закупка
    positionNumber - Реестровый номер позиции в плане-графике закупок. От ЕИС
    extNumber - Внешний номер позиции
    IKZ - Идентификационный код закупки
    publishYear - Планируемый год размещения извещения
    IKU - Идентификационный код организации-владельца версии плана-графика закупок
    purchaseNumber -Номер закупки, включенной в план-график закупок
    """

    tree = open_xml(outgoing_xml)
    template = ET.ElementTree(file="templates/tenderPlan2020.xml")

    template.find('.//ns3:id', ns).text = template.find('.//ns3:id', ns).text[:-4] + str(randint(1000, 9999))
    template.find('.//ns3:externalId', ns).text = tree.find('.//ns3:externalId', ns).text
    template.find('.//ns3:planNumber', ns).text = tree.find('.//ns3:planNumber', ns).text
    template.find('.//ns3:versionNumber', ns).text = tree.find('.//ns3:versionNumber', ns).text
    template.find('.//ns3:confirmDate', ns).text = tree.find('.//ns1:createDateTime', ns).text

    count_position = len(tree.findall('.//ns3:positions/ns3:position', ns))

    if count_position > 0:

        member = copy.deepcopy(template.find(".//ns4:tenderPlan2020/ns3:positions/ns3:position", ns))
        [template.find(".//ns3:positions", ns).append(member) for i in range(count_position)]

        for i in range(count_position):
            template.findall('.//ns3:commonInfo/ns3:positionNumber', ns)[i].text = template.findall(
                './/ns3:commonInfo/ns3:positionNumber', ns)[i].text[:-4] + str(randint(1000, 9999))

            template.findall('.//ns3:commonInfo/ns3:extNumber', ns)[i].text = tree.findall(
                './/ns3:commonInfo/ns3:extNumber', ns)[i].text

            try:
                template.findall('.//ns3:commonInfo/ns3:IKZ', ns)[i].text = tree.findall(
                    './/ns3:commonInfo/ns3:IKZ', ns)[i].text
            except (AttributeError, IndexError):
                template.findall('.//ns3:commonInfo/ns3:IKZ', ns)[i].text = template.findall(
                    './/ns3:commonInfo/ns3:IKZ', ns)[i].text[:-4] + str(randint(1000, 9999))

            template.findall('.//ns3:commonInfo/ns3:publishYear', ns)[i].text = tree.findall(
                './/ns3:commonInfo/ns3:publishYear', ns)[i].text

            try:
                template.findall(f'.//ns3:commonInfo/ns3:IKU', ns)[i].text = tree.findall(
                    './/ns3:commonInfo/ns3:IKU', ns)[i].text
            except AttributeError:
                template.findall(f'.//ns3:commonInfo/ns3:IKU', ns)[i].text = tree.findall(
                    f'.//ns3:commonInfo/ns3:IKU', ns)[i].text[:-4] + str(randint(1000, 9999))

            template.findall(f'.//ns3:commonInfo/ns3:purchaseNumber', ns)[i].text = tree.findall(
                './/ns3:commonInfo/ns3:purchaseNumber', ns)[i].text

    else:

        member = template.find(".//ns4:tenderPlan2020", ns)
        member.remove(template.find(".//ns3:positions", ns))

    count_special_position = len(tree.findall('.//ns3:specialPurchasePosition', ns))
    if count_special_position > 0:

        member = copy.deepcopy(template.find(".//ns3:specialPurchasePosition", ns))
        [template.find(".//ns3:specialPurchasePositions", ns).append(member) for i in range(count_special_position - 1)]

        for i in range(count_special_position):

            template.findall('.//ns3:specialPurchasePosition/ns3:positionNumber', ns)[i].text = \
                template.findall('.//ns3:specialPurchasePosition/ns3:positionNumber', ns)[i].text[:-4] + str(
                    randint(1000, 9999))

            template.findall('.//ns3:specialPurchasePosition/ns3:extNumber', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition/ns3:extNumber', ns)[i].text

            try:
                template.findall('.//ns3:specialPurchasePosition/ns3:IKZ', ns)[i].text = tree.findall(
                    './/ns3:specialPurchasePosition/ns3:IKZ', ns)[i].text
            except AttributeError:
                template.findall('.//ns3:specialPurchasePosition/ns3:IKZ', ns)[i].text = tree.findall(
                    './/ns3:specialPurchasePosition/ns3:IKZ', ns)[i].text[:-4] + str(randint(1000, 9999))

            template.findall('.//ns3:specialPurchasePosition/ns3:publishYear', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition/ns3:publishYear', ns)[i].text

            try:
                template.findall(f'.//ns3:specialPurchasePosition/ns3:IKU', ns)[i].text = tree.findall(
                    './/ns3:specialPurchasePosition/ns3:IKU', ns)[i].text
            except AttributeError:
                template.findall(f'.//ns3:specialPurchasePosition/ns3:IKU', ns)[i].text = tree.findall(
                    f'.//ns3:specialPurchasePosition/ns3:IKU', ns)[i].text[:-4] + str(randint(1000, 9999))

            template.findall(f'.//ns3:specialPurchasePosition/ns3:purchaseNumber', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition/ns3:purchaseNumber', ns)[i].text
    else:

        member = template.find(".//ns4:tenderPlan2020", ns)
        member.remove(template.find(".//ns3:specialPurchasePositions", ns))

    create_xml(template)
