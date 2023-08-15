import copy
import xml.etree.ElementTree as ET
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml, random_number


def tender_plan_2020(outgoing_xml):
    """Добавление позиции (особой позиции) в опубликованный в ЕИС план-график"""

    template = ET.ElementTree(file='templates/tenderPlan2020.xml').getroot()
    tree = open_xml(outgoing_xml).getroot()
    count_position = len(tree.findall('.//ns3:positions/ns3:position', ns))
    count_special_position = len(tree.findall(f'.//ns3:specialPurchasePosition', ns))

    if count_position == 0:
        template.find('.//ns4:tenderPlan2020', ns).remove(template.find('.//ns3:positions', ns))
    elif count_position > 1:
        member = copy.deepcopy(template.find('.//ns4:tenderPlan2020/ns3:positions/ns3:position', ns))
        for i in range(2, count_position + 1):
            template.find(".//ns3:positions", ns).insert(i, member)

    if count_special_position == 0:
        template.find('.//ns4:tenderPlan2020', ns).remove(template.find('.//ns3:specialPurchasePositions', ns))
    elif count_special_position > 1:
        member = copy.deepcopy(template.find('.//ns3:specialPurchasePosition', ns))
        for i in range(2, count_special_position + 1):
            template.find('.//ns3:specialPurchasePositions', ns).insert(i, member)

    temp = ET.ElementTree(template)
    temp.write('venv/temp.xml', encoding='utf-8', xml_declaration=True)
    template = ET.ElementTree(file='venv/temp.xml').getroot()

    template.find('.//ns3:id', ns).text = random_number(8)
    template.find('.//ns3:externalId', ns).text = tree.find('.//ns3:externalId', ns).text
    template.find('.//ns3:planNumber', ns).text = tree.find('.//ns3:planNumber', ns).text
    template.find('.//ns3:versionNumber', ns).text = tree.find('.//ns3:versionNumber', ns).text
    template.find('.//ns3:confirmDate', ns).text = tree.find('.//ns1:createDateTime', ns).text

    for i in range(1, count_position + 1):

        try:
            template.find(f'.//ns3:commonInfo[{i}]/ns3:positionNumber', ns).text = tree.find(
                f'.//ns3:commonInfo[{i}]/ns3:positionNumber', ns).text
        except AttributeError:
            template.find(f'.//ns3:commonInfo[{i}]/ns3:positionNumber', ns).text = random_number(24)
        try:
            template.find(f'.//ns3:commonInfo[{i}]/ns3:IKZ', ns).text = tree.find(
                f'.//ns3:commonInfo[{i}]/ns3:IKZ', ns).text
        except AttributeError:
            template.find(f'.//ns3:commonInfo[{i}]/ns3:IKZ', ns).text = random_number(36)

        template.find(f'.//ns3:commonInfo[{i}]/ns3:extNumber', ns).text = tree.find(
            f'.//ns3:commonInfo[{i}]/ns3:extNumber', ns).text
        template.find(f'.//ns3:commonInfo[{i}]/ns3:publishYear', ns).text = tree.find(
            f'.//ns3:commonInfo[{i}]/ns3:publishYear', ns).text
        template.find(f'.//ns3:commonInfo[{i}]/ns3:IKU', ns).text = tree.find(
            f'.//ns3:commonInfo[{i}]/ns3:IKU', ns).text
        template.find(f'.//ns3:commonInfo[{i}]/ns3:purchaseNumber', ns).text = tree.find(
            f'.//ns3:commonInfo[{i}]/ns3:purchaseNumber', ns).text

    for i in range(1, count_special_position + 1):
        try:
            template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:positionNumber', ns).text = tree.find(
                f'.//ns3:specialPurchasePosition[{i}]/ns3:positionNumber', ns).text
        except AttributeError:
            template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:positionNumber', ns).text = random_number(24)
        try:
            template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:IKZ', ns).text = tree.find(
                f'.//ns3:specialPurchasePosition[{i}]/ns3:IKZ', ns).text
        except AttributeError:
            template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:IKZ', ns).text = random_number(36)

        template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:extNumber', ns).text = tree.find(
            f'.//ns3:specialPurchasePosition[{i}]/ns3:extNumber', ns).text
        template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:publishYear', ns).text = tree.find(
            f'.//ns3:specialPurchasePosition[{i}]/ns3:publishYear', ns).text
        template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:IKU', ns).text = tree.find(
            f'.//ns3:specialPurchasePosition[{i}]/ns3:IKU', ns).text
        template.find(f'.//ns3:specialPurchasePosition[{i}]/ns3:purchaseNumber', ns).text = tree.find(
            f'.//ns3:specialPurchasePosition[{i}]/ns3:purchaseNumber', ns).text

    create_xml(ET.ElementTree(template), outgoing_xml.split("/")[-1:][0][:2])
