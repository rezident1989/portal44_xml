import copy

from src.namespace import namespace as ns
from src.system_functions import (open_xml, random_number, create_xml, validate_xsd, to_sent_to_sftp,
                                  current_date_and_time)


def ef_protocol_submit_offers(data, send=True):
    """Протокол подачи ценовых предложений ЭА20.
    Новый статус: Работа комиссии (подведение итогов)"""

    template = open_xml("templates/protocols/EF2020/epProtocolEF2020SubmitOffers_altova.xml")

    template.find('.//ns4:epProtocolEF2020SubmitOffers', ns).attrib = data.schema_version

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = data.external_id
    template.find('.//ns5:versionNumber', ns).text = data.version_number
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = data.purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = data.publish_in_eis
    template.find('.//ns5:procedureDT', ns).text = data.publish_in_eis
    template.find('.//ns5:signDT', ns).text = current_date_and_time()

    xml = create_xml(template)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, data.server_address)


def ef_protocol_final_part(data, send=True):
    """Протокол подведения итогов определения поставщика (подрядчика, исполнителя) ЭА20
    Новый статус: Заключение контракта"""

    template = open_xml("templates/protocols/EF2020/epProtocolEF2020FinalPart_altova.xml")

    template.find('.//ns4:epProtocolEF2020FinalPart', ns).attrib = data.schema_version

    template.find('.//ns5:id', ns).text = random_number(8)
    template.find('.//ns5:externalId', ns).text = data.external_id
    template.find('.//ns5:versionNumber', ns).text = data.version_number
    template.find('.//ns5:commonInfo/ns5:purchaseNumber', ns).text = data.purchase_number
    template.find('.//ns5:publishDTInETP', ns).text = data.publish_in_eis
    template.find('.//ns5:procedureDT', ns).text = data.publish_in_eis
    template.find('.//ns5:signDT', ns).text = current_date_and_time()

    data.purchase_protocol_sid = tuple(
        random_number(8) for _ in range(len(data.purchase_objects_sid)))

    data.drug_protocol_sid = tuple(
        random_number(8) for _ in range(len(data.drug_purchase_objects_sid)))

    a = template.find('.//ns5:proposalsInfo', ns)
    b = template.find('.//ns5:notDrugProposalsInfo', ns)
    c = template.find('.//ns5:drugProposalsInfo', ns)

    if len(data.purchase_objects_sid) > 0:
        a.remove(c)
        for _ in range(1, len(data.purchase_objects_sid)):
            b.insert(0, copy.deepcopy(template.find('.//ns5:productInfo', ns)))
        for i, not_drug_proposals_info in enumerate(
                template.findall('.//ns5:productInfo/ns5:sid', ns)):
            not_drug_proposals_info.text = data.purchase_protocol_sid[i]
        for i, not_drug_proposals_info in enumerate(
                template.findall('.//ns5:productInfo/ns5:notificationSid', ns)):
            not_drug_proposals_info.text = data.purchase_objects_sid[i]
        for i, not_drug_proposals_info in enumerate(
                template.findall('.//ns5:productInfo/ns5:notificationExternalSId', ns)):
            not_drug_proposals_info.text = data.purchase_objects_external_sid[i]

    else:
        a.remove(b)
        for _ in range(1, len(data.drug_purchase_objects_sid)):
            c.insert(0, copy.deepcopy(template.find('.//ns5:drugProductInfo', ns)))
        for i, drug_proposals_info in enumerate(
                template.findall('.//ns5:drugProductInfo/ns5:sid', ns)):
            drug_proposals_info.text = data.drug_purchase_protocol_sid[i]
        for i, drug_proposals_info in enumerate(
                template.findall('.//ns5:drugProductInfo/ns5:notificationSid', ns)):
            drug_proposals_info.text = data.drug_purchase_objects_sid[i]
        for i, drug_proposals_info in enumerate(
                template.findall('.//ns5:drugProductInfo/ns5:notificationExternalSId', ns)):
            drug_proposals_info.text = data.drug_external_sid[i]

    xml = create_xml(template)
    validate_xsd(xml)
    if send:
        to_sent_to_sftp(xml, data.server_address)
