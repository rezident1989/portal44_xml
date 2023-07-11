import xml.etree.ElementTree as ET
from random import randint
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml


def tender_plan_2020(outgoing_xml):
    """План-график начиная с 2020 года"""

    tree = open_xml(outgoing_xml)

    template = ET.ElementTree(file="templates/tender_plan_2020.xml")

    # Идентификатор ревизии плана-графика. ЕИС
    template.find('.//ns3:id', ns).text = template.find('.//ns3:id', ns).text[:-4] + str(randint(1000, 9999))

    # Внешний идентификатор плана-графика. ИМЦ
    template.find('.//ns3:externalId', ns).text = tree.find('.//ns3:externalId', ns).text

    # Реестровый номер плана-графика. ИМЦ
    try:
        template.find('.//ns3:planNumber', ns).text = tree.find('.//ns3:planNumber', ns).text
    except AttributeError:
        template.find('.//ns3:planNumber', ns).text = template.find('.//ns3:planNumber', ns).text[:-4] + str(
            randint(1000, 9999))

    # Номер версии плана-графика. ИМЦ
    template.find('.//ns3:versionNumber', ns).text = tree.find('.//ns3:versionNumber', ns).text

    # Дата утверждения версии плана-графика. ИМЦ
    template.find('.//ns3:confirmDate', ns).text = tree.find('.//ns1:createDateTime', ns).text

    # Дата размещения версии плана-графика. ИМЦ
    template.find('.//ns3:publishDate', ns).text = tree.find('.//ns1:createDateTime', ns).text

    count_position = len(tree.findall('.//ns3:position', ns))
    if count_position > 0:
        for i in range(count_position):

            # Реестровый номер ПОЗИЦИИ в плане-графике. ЕИС
            template.findall('.//ns3:commonInfo//ns3:positionNumber', ns)[i].text = template.findall(
                './/ns3:commonInfo//ns3:positionNumber', ns)[i].text[:-4] + str(randint(1000, 9999))

            # Внешний номер ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:commonInfo//ns3:extNumber', ns)[i].text = tree.findall(
                './/ns3:commonInfo//ns3:extNumber', ns)[i].text

            # Идентификационный код закупки ПОЗИЦИИ плана-графика. ИМЦ
            try:
                template.findall('.//ns3:commonInfo//ns3:IKZ', ns)[i].text = tree.findall(
                    './/ns3:commonInfo//ns3:IKZ', ns)[i].text
            except (AttributeError, IndexError):
                pass

            # Планируемый год размещения ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:commonInfo//ns3:publishYear', ns)[i].text = tree.findall(
                './/ns3:commonInfo//ns3:publishYear', ns)[i].text

            # Идентификационный код организации-владельца. ИМЦ
            template.findall(f'.//ns3:commonInfo//ns3:IKU', ns)[i].text = tree.findall(
                './/ns3:commonInfo//ns3:IKU', ns)[i].text

            # Номер закупки. ИМЦ
            template.findall(f'.//ns3:commonInfo//ns3:purchaseNumber', ns)[i].text = tree.findall(
                './/ns3:commonInfo//ns3:purchaseNumber', ns)[i].text

    count_special_position = len(tree.findall('.//ns3:specialPurchasePosition', ns))
    if count_special_position > 0:
        for i in range(count_special_position):

            # Реестровый номер ПОЗИЦИИ в плане-графике. ЕИС
            template.findall('.//ns3:specialPurchasePosition//ns3:positionNumber', ns)[i].text = \
                template.findall('.//ns3:specialPurchasePosition//ns3:positionNumber', ns)[i].text[:-4] + str(
                    randint(1000, 9999))

            # Внешний номер ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:specialPurchasePosition//ns3:extNumber', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition//ns3:extNumber', ns)[i].text

            # Идентификационный код закупки ПОЗИЦИИ плана-графика. ИМЦ
            try:
                template.findall('.//ns3:specialPurchasePosition//ns3:IKZ', ns)[i].text = tree.findall(
                    './/ns3:specialPurchasePosition//ns3:IKZ', ns)[i].text
            except (AttributeError, IndexError):
                pass

            # Планируемый год размещения ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:specialPurchasePosition//ns3:publishYear', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition//ns3:publishYear', ns)[i].text

            # Идентификационный код организации-владельца. ИМЦ
            template.findall(f'.//ns3:specialPurchasePosition//ns3:IKU', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition//ns3:IKU', ns)[i].text

            # Номер закупки. ИМЦ
            template.findall(f'.//ns3:specialPurchasePosition//ns3:purchaseNumber', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition//ns3:purchaseNumber', ns)[i].text

    create_xml(template)
