import copy
import xml.etree.ElementTree as ET
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml, random_number


def tender_plan_2020(outgoing_xml):
    """Добавление позиции (особой позиции) в опубликованный в ЕИС план-график"""

    tree = open_xml(outgoing_xml).getroot()
    template = ET.ElementTree(file="templates/tenderPlan2020.xml").getroot()

    template.find('.//ns3:id', ns).text = random_number(8)
    template.find('.//ns3:externalId', ns).text = tree.find('.//ns3:externalId', ns).text
    template.find('.//ns3:planNumber', ns).text = tree.find('.//ns3:planNumber', ns).text
    template.find('.//ns3:versionNumber', ns).text = tree.find('.//ns3:versionNumber', ns).text
    template.find('.//ns3:confirmDate', ns).text = tree.find('.//ns1:createDateTime', ns).text

    count_position = len(tree.findall('.//ns3:positions/ns3:position', ns))

    if count_position > 0:

        if count_position > 1:
            member = copy.deepcopy(template.find(".//ns4:tenderPlan2020/ns3:positions/ns3:position", ns))
            [template.find(".//ns3:positions", ns).append(member) for i in range(count_position - 1)]

        for i in range(count_position):

            try:
                template.findall('.//ns3:commonInfo/ns3:positionNumber', ns)[i].text = tree.findall(
                    './/ns3:commonInfo/ns3:positionNumber', ns)[i].text
            except (AttributeError, IndexError):
                template.findall('.//ns3:commonInfo/ns3:positionNumber', ns)[i].text = random_number(24)

            template.findall('.//ns3:commonInfo/ns3:extNumber', ns)[i].text = tree.findall(
                './/ns3:commonInfo/ns3:extNumber', ns)[i].text

            try:
                template.findall('.//ns3:commonInfo/ns3:IKZ', ns)[i].text = tree.findall(
                    './/ns3:commonInfo/ns3:IKZ', ns)[i].text
            except (AttributeError, IndexError):
                template.findall('.//ns3:commonInfo/ns3:IKZ', ns)[i].text = random_number(36)

            template.findall('.//ns3:commonInfo/ns3:publishYear', ns)[i].text = tree.findall(
                './/ns3:commonInfo/ns3:publishYear', ns)[i].text

            # TODO
            # try:
            template.findall(f'.//ns3:commonInfo/ns3:IKU', ns)[i].text = tree.findall(
                './/ns3:commonInfo/ns3:IKU', ns)[i].text
            # except AttributeError:
            # template.findall(f'.//ns3:commonInfo/ns3:IKU', ns)[i].text = random_number(20)

            template.findall(f'.//ns3:commonInfo/ns3:purchaseNumber', ns)[i].text = tree.findall(
                './/ns3:commonInfo/ns3:purchaseNumber', ns)[i].text

    else:
        member = template.find(".//ns4:tenderPlan2020", ns)
        member.remove(template.find(".//ns3:positions", ns))

    count_special_position = len(tree.findall('.//ns3:specialPurchasePosition', ns))
    if count_special_position > 0:

        if count_special_position > 1:
            member = copy.deepcopy(template.find(".//ns3:specialPurchasePosition", ns))
            [template.find(".//ns3:specialPurchasePositions", ns).append(
                member) for i in range(count_special_position - 1)]

        for i in range(count_special_position):

            try:
                template.findall('.//ns3:specialPurchasePosition/ns3:positionNumber', ns)[i].text = tree.findall(
                    '//ns3:specialPurchasePosition/ns3:positionNumber', ns)[i].text
            except (AttributeError, IndexError):
                template.findall('.//ns3:specialPurchasePosition/ns3:positionNumber', ns)[i].text = random_number(24)

            template.findall('.//ns3:specialPurchasePosition/ns3:extNumber', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition/ns3:extNumber', ns)[i].text
            try:
                template.findall('.//ns3:specialPurchasePosition/ns3:IKZ', ns)[i].text = tree.findall(
                    './/ns3:specialPurchasePosition/ns3:IKZ', ns)[i].text
            except (AttributeError, IndexError):
                template.findall('.//ns3:specialPurchasePosition/ns3:IKZ', ns)[i].text = random_number(36)
            template.findall('.//ns3:specialPurchasePosition/ns3:publishYear', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition/ns3:publishYear', ns)[i].text

            # TODO
            # try:
            template.findall(f'.//ns3:specialPurchasePosition/ns3:IKU', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition/ns3:IKU', ns)[i].text
            # except AttributeError:
            # template.findall(f'.//ns3:specialPurchasePosition/ns3:IKU', ns)[i].text = random_number(20)

            template.findall(f'.//ns3:specialPurchasePosition/ns3:purchaseNumber', ns)[i].text = tree.findall(
                './/ns3:specialPurchasePosition/ns3:purchaseNumber', ns)[i].text

    else:
        member = template.find(".//ns4:tenderPlan2020", ns)
        member.remove(template.find(".//ns3:specialPurchasePositions", ns))

    create_xml(ET.ElementTree(template), outgoing_xml.split("/")[-1:][0][:2])
