import datetime
import xml.etree.ElementTree as ET
import re
from random import randint

ns = {'ns1': 'http://zakupki.gov.ru/oos/integration/1',
      'ns2': "http://zakupki.gov.ru/oos/types/1",
      'ns3': "http://zakupki.gov.ru/oos/TPtypes/1"
      }


def open_xml(path):
    """Открывает xml_bag-файл и возвращает его структуру(tree)"""
    tree = ET.ElementTree(file=path)
    return tree


def create_xml(tree):
    """Создает xml-файл"""
    name_file = re.findall(r'[}]\w+', tree.getroot()[0].tag)
    a = "".join(name_file).replace('}', '')
    tree.write(
        f'outgoing/{datetime.datetime.now().strftime("%H.%M_%d.%m.%y_")}{a}.xml', encoding='utf-8',
        xml_declaration=True)


def confirm(outgoing_xml):
    """Меняет текст тегов в дереве шаблона на текст тегов из дерева исходящего файла"""

    # Шаблон пакета
    template = ET.ElementTree(file="templates/confirmation.xml")

    # Глобальный идентификатор информационного пакета. ЕИС
    template.find('.//ns1:id', ns).text = template.find('.//ns1:id', ns).text[:-4] + str(randint(1000, 9999))

    # Номер текущей сессии. ЕИС
    template.find('.//ns2:loadId', ns).text = str(randint(10000000, 99999999))

    # Глобальный идентификатор информационного пакета. ИМЦ
    template.find('.//ns2:refId', ns).text = outgoing_xml.find('.//ns1:id', ns).text

    return template


def tender_plan_2020(outgoing_xml):
    """Меняет текст тегов в дереве шаблона на текст тегов из дерева исходящего файла"""

    template = ET.ElementTree(file="templates/tender_plan_2020.xml")

    # Идентификатор ревизии плана-графика. ЕИС
    template.find('.//ns3:id', ns).text = template.find('.//ns3:id', ns).text[:-4] + str(randint(1000, 9999))

    # Внешний идентификатор плана-графика. ИМЦ
    template.find('.//ns3:externalId', ns).text = outgoing_xml.find('.//ns3:externalId', ns).text

    # Реестровый номер плана-графика. ИМЦ
    try:
        template.find('.//ns3:planNumber', ns).text = outgoing_xml.find('.//ns3:planNumber', ns).text
    except AttributeError:
        template.find('.//ns3:planNumber', ns).text = template.find('.//ns3:planNumber', ns).text[:-4] + str(
            randint(1000, 9999))

    # Номер версии плана-графика. ИМЦ
    template.find('.//ns3:versionNumber', ns).text = outgoing_xml.find('.//ns3:versionNumber', ns).text

    # Дата утверждения версии плана-графика. ИМЦ
    template.find('.//ns3:confirmDate', ns).text = outgoing_xml.find('.//ns1:createDateTime', ns).text

    # Дата размещения версии плана-графика. ИМЦ
    template.find('.//ns3:publishDate', ns).text = outgoing_xml.find('.//ns1:createDateTime', ns).text

    count_position = len(outgoing_xml.findall('.//ns3:position', ns))
    if count_position > 0:
        for i in range(count_position):

            # Реестровый номер ПОЗИЦИИ в плане-графике. ЕИС
            template.findall('.//ns3:commonInfo//ns3:positionNumber', ns)[i].text = template.findall(
                './/ns3:commonInfo//ns3:positionNumber', ns)[i].text[:-4] + str(randint(1000, 9999))

            # Внешний номер ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:commonInfo//ns3:extNumber', ns)[i].text = outgoing_xml.findall(
                './/ns3:commonInfo//ns3:extNumber', ns)[i].text

            # Идентификационный код закупки ПОЗИЦИИ плана-графика. ИМЦ
            try:
                template.findall('.//ns3:commonInfo//ns3:IKZ', ns)[i].text = outgoing_xml.findall(
                    './/ns3:commonInfo//ns3:IKZ', ns)[i].text
            except (AttributeError, IndexError):
                pass

            # Планируемый год размещения ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:commonInfo//ns3:publishYear', ns)[i].text = outgoing_xml.findall(
                './/ns3:commonInfo//ns3:publishYear', ns)[i].text

            # Идентификационный код организации-владельца. ИМЦ
            template.findall(f'.//ns3:commonInfo//ns3:IKU', ns)[i].text = outgoing_xml.findall(
                './/ns3:commonInfo//ns3:IKU', ns)[i].text

            # Номер закупки. ИМЦ
            template.findall(f'.//ns3:commonInfo//ns3:purchaseNumber', ns)[i].text = outgoing_xml.findall(
                './/ns3:commonInfo//ns3:purchaseNumber', ns)[i].text

    count_special_position = len(outgoing_xml.findall('.//ns3:specialPurchasePosition', ns))
    if count_position > 0:
        for i in range(count_special_position):

            # Реестровый номер ПОЗИЦИИ в плане-графике. ЕИС
            template.findall('.//ns3:specialPurchasePosition//ns3:positionNumber', ns)[i].text = template.findall(
                './/ns3:specialPurchasePosition//ns3:positionNumber', ns)[i].text[:-4] + str(randint(1000, 9999))

            # Внешний номер ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:specialPurchasePosition//ns3:extNumber', ns)[i].text = outgoing_xml.findall(
                './/ns3:specialPurchasePosition//ns3:extNumber', ns)[i].text

            # Идентификационный код закупки ПОЗИЦИИ плана-графика. ИМЦ
            try:
                template.findall('.//ns3:specialPurchasePosition//ns3:IKZ', ns)[i].text = outgoing_xml.findall(
                    './/ns3:specialPurchasePosition//ns3:IKZ', ns)[i].text
            except (AttributeError, IndexError):
                pass

            # Планируемый год размещения ПОЗИЦИИ плана-графика. ИМЦ
            template.findall('.//ns3:specialPurchasePosition//ns3:publishYear', ns)[i].text = outgoing_xml.findall(
                './/ns3:specialPurchasePosition//ns3:publishYear', ns)[i].text

            # Идентификационный код организации-владельца. ИМЦ
            template.findall(f'.//ns3:specialPurchasePosition//ns3:IKU', ns)[i].text = outgoing_xml.findall(
                './/ns3:specialPurchasePosition//ns3:IKU', ns)[i].text

            # Номер закупки. ИМЦ
            template.findall(f'.//ns3:specialPurchasePosition//ns3:purchaseNumber', ns)[i].text = outgoing_xml.findall(
                './/ns3:specialPurchasePosition//ns3:purchaseNumber', ns)[i].text

    return template


if __name__ == '__main__':

    file_path = 'incoming/14433406_xml.xml'
    create_xml(confirm(open_xml(file_path)))
    create_xml(tender_plan_2020(open_xml(file_path)))
