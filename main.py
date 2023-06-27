import datetime
from random import randint
import xml.etree.ElementTree as ET
import re


def open_xml(path):
    """Открывает xml_bag-файл и возвращает его структуру(tree)"""
    tree = ET.ElementTree(file=path)
    return tree


def create_xml(tree):
    """Создает xml_bag-файл"""
    name_file = re.findall(r'[}]\w+', tree.getroot()[0].tag)
    a = "".join(name_file).replace('}', '')
    tree.write(
        f'outgoing/{datetime.datetime.now().strftime("%H.%M_%d.%m.%y_")}{a}.xml', encoding='utf-8',
        xml_declaration=True)


def confirmation(tree_template, tree_outgoing):
    """Меняет текст тегов в дереве шаблона на текст тегов из дерева исходящего файла"""
    ns = {'integration': 'http://zakupki.gov.ru/oos/integration/1',
          'types': "http://zakupki.gov.ru/oos/types/1"
          }
    tag_list = []

    id_tag = tree_template.find('.//integration:id', ns)
    id_tag.text = id_tag.text[:-4] + str(randint(1000, 9999))
    tag_list.append(id_tag)
    # глобальный идентификатор информационного пакета от ЕИС

    loadId_tag = tree_template.find('.//types:loadId', ns)
    loadId_tag.text = str(randint(10000000, 99999999))
    tag_list.append(loadId_tag)
    # номер текущей сессии с ЕИС

    refId_tag = tree_template.find('.//types:refId', ns)
    refId_tag.text = tree_outgoing.find('.//integration:id', ns).text
    tag_list.append(refId_tag)
    # глобальный идентификатор информационного пакета от ИМЦ

    print('\nДобавлены следующие теги:')
    for i in tag_list:
        print(i.tag, '\t', i.text)

    return tree_template


def tender_plan_2020(tree_template, tree_outgoing):
    """Меняет текст тегов в дереве шаблона на текст тегов из дерева исходящего файла"""

    ns = {'TPtypes': 'http://zakupki.gov.ru/oos/TPtypes/1',
          'integration': 'http://zakupki.gov.ru/oos/integration/1'
          }
    tag_list = []

    id_tag = tree_template.find('.//TPtypes:id', ns)
    id_tag.text = id_tag.text[:-4] + str(randint(1000, 9999))
    tag_list.append(id_tag)
    # идентификатор ревизии плана-графика от ЕИС

    externalId_tag = tree_template.find('.//TPtypes:externalId', ns)
    externalId_tag.text = tree_outgoing.find('.//TPtypes:externalId', ns).text
    tag_list.append(externalId_tag)
    # внешний идентификатор плана-графика от ИМЦ

    planNumber_tag = tree_template.find('.//TPtypes:planNumber', ns)
    planNumber_tag.text = tree_outgoing.find('.//TPtypes:planNumber', ns).text
    tag_list.append(planNumber_tag)
    # реестровый номер плана-графика от ИМЦ

    versionNumber_tag = tree_template.find('.//TPtypes:versionNumber', ns)
    versionNumber_tag.text = tree_outgoing.find('.//TPtypes:versionNumber', ns).text
    tag_list.append(versionNumber_tag)
    # номер версии плана-графика от ИМЦ

    confirmDate_tag = tree_template.find('.//TPtypes:confirmDate', ns)
    confirmDate_tag.text = tree_outgoing.find('.//integration:createDateTime', ns).text
    tag_list.append(confirmDate_tag)
    # дата утверждения версии плана-графика от ИМЦ

    publishDate_tag = tree_template.find('.//TPtypes:publishDate', ns)
    publishDate_tag.text = tree_outgoing.find('.//integration:createDateTime', ns).text
    tag_list.append(publishDate_tag)
    # дата размещения версии плана-графика от ИМЦ

    positionNumber_tag = tree_template.find('.//TPtypes:commonInfo//TPtypes:positionNumber', ns)
    positionNumber_tag.text = positionNumber_tag.text[:-4] + str(randint(1000, 9999))
    tag_list.append(positionNumber_tag)
    # реестровый номер ПОЗИЦИИ в плане-графике от ЕИС

    extNumber_tag = tree_template.find('.//TPtypes:commonInfo//TPtypes:extNumber', ns)
    extNumber_tag.text = tree_outgoing.find('.//TPtypes:commonInfo//TPtypes:extNumber', ns).text
    tag_list.append(extNumber_tag)
    # внешний номер ПОЗИЦИИ плана-графика от ИМЦ

    IKZ_tag = tree_template.find('.//TPtypes:commonInfo//TPtypes:IKZ', ns)
    try:
        IKZ_tag.text = tree_outgoing.find('.//TPtypes:commonInfo//TPtypes:IKZ', ns).text
        tag_list.append(IKZ_tag)
    except AttributeError:
        print('\nТэг {IKZ_tag} удален, так как не найден во входящем'.format(IKZ_tag=IKZ_tag.tag))
        all_tag = tree_template.find('.//TPtypes:position//TPtypes:commonInfo', ns)
        all_tag.remove(IKZ_tag)
    # идентификационный код закупки ПОЗИЦИИ плана-графика от ИМЦ

    publishYear_tag = tree_template.find('.//TPtypes:commonInfo//TPtypes:publishYear', ns)
    publishYear_tag.text = tree_outgoing.find('.//TPtypes:commonInfo//TPtypes:publishYear', ns).text
    tag_list.append(publishYear_tag)
    # планируемый год размещения ПОЗИЦИИ плана-графика от ИМЦ

    IKU_tag = tree_template.find('.//TPtypes:commonInfo//TPtypes:IKU', ns)
    IKU_tag.text = tree_outgoing.find('.//TPtypes:commonInfo//TPtypes:IKU', ns).text
    tag_list.append(IKU_tag)
    # Идентификационный код организации-владельца от ИМЦ

    purchaseNumber_tag = tree_template.find('.//TPtypes:commonInfo//TPtypes:purchaseNumber', ns)
    purchaseNumber_tag.text = tree_outgoing.find('.//TPtypes:commonInfo//TPtypes:purchaseNumber', ns).text
    tag_list.append(purchaseNumber_tag)
    # Идентификационный код организации-владельца от ИМЦ

    print('\nДобавлены следующие теги:')
    for i in tag_list:
        print(i.tag, '\t', i.text)

    return tree_templ


if __name__ == '__main__':
    tree_out = open_xml('incoming/14433401_xml.xml')

    tree_templ = open_xml('templates/confirmation.xml')
    create_xml(confirmation(tree_templ, tree_out))

    tree_templ = open_xml('templates/tender_plan_2020.xml')
    create_xml(tender_plan_2020(tree_templ, tree_out))
