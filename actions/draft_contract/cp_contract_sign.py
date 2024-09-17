from src.namespace import namespace as ns

from src.system_functions import open_xml, random_number, create_xml, to_sent_to_sftp, get_server_address, validate_xsd


def cp_contract_sign(outgoing_xml, send=True):
    """----"""

    outgoing = open_xml(outgoing_xml)

    template = open_xml("templates/draft_contract/cpContractSign.xml")

    template.find('.//ns7:id', ns).text = random_number(8)
    template.find('.//ns7:purchaseNumber', ns).text = outgoing.find('.//ns7:purchaseNumber', ns).text
    template.find('.//ns7:purchaseCode', ns).text = outgoing.find('.//ns7:purchaseCode', ns).text

    xml = create_xml(template)
    a = get_server_address(outgoing_xml)
    to_sent_to_sftp(xml, a)
