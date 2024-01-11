import copy
from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, random_number


def tender_plan_2020(outgoing_xml):
    """Добавление позиции (особой позиции) в опубликованный в ЕИС план-график"""

    template = open_xml('src/templates/tenderPlan2020.xml')
    tree = open_xml(outgoing_xml)

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
        for i in range(2, count_special_position + 1):
            member = copy.deepcopy(template.find('.//ns3:specialPurchasePosition', ns))
            template.find('.//ns3:specialPurchasePositions', ns).insert(i, member)

    template.find('.//ns3:id', ns).text = random_number(8)
    template.find('.//ns3:externalId', ns).text = tree.find('.//ns3:externalId', ns).text

    try:
        template.find('.//ns3:planNumber', ns).text = tree.find('.//ns3:planNumber', ns).text
    except AttributeError:
        template.find('.//ns3:planNumber', ns).text = '2024' + str(random_number(14))

    template.find('.//ns3:versionNumber', ns).text = tree.find('.//ns3:versionNumber', ns).text
    template.find('.//ns3:confirmDate', ns).text = tree.find('.//ns1:createDateTime', ns).text
    template.find('.//ns3:publishDate', ns).text = tree.find('.//ns1:createDateTime', ns).text

    template_purchase = (template.findall('.//ns3:position/ns3:commonInfo/..', ns)
                         + template.findall('.//ns3:specialPurchasePosition', ns))
    tree_purchase = (tree.findall('.//ns3:position/ns3:commonInfo/..', ns)
                     + tree.findall('.//ns3:specialPurchasePosition', ns))

    for i1, tag_temp in enumerate(template_purchase):
        for i2, tag_three in enumerate(tree_purchase):
            if i1 == i2:
                try:
                    tag_temp.find('.//ns3:positionNumber', ns).text = tag_three.find('.//ns3:positionNumber', ns).text
                    tag_temp.find('.//ns3:IKZ', ns).text = tag_three.find('.//ns3:IKZ', ns).text
                except AttributeError:
                    tag_temp.find('.//ns3:positionNumber', ns).text = f'23{random_number(22)}'
                    tag_temp.find('.//ns3:IKZ', ns).text = f'23{random_number(34)}'
                tag_temp.find('.//ns3:extNumber', ns).text = tag_three.find('.//ns3:extNumber', ns).text
                tag_temp.find('.//ns3:publishYear', ns).text = tag_three.find('.//ns3:publishYear', ns).text
                tag_temp.find('.//ns3:IKU', ns).text = tag_three.find('.//ns3:IKU', ns).text
                tag_temp.find('.//ns3:purchaseNumber', ns).text = tag_three.find('.//ns3:purchaseNumber', ns).text

    return template
