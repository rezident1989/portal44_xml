from src.namespace import namespace as ns

from src.system_functions import open_xml, random_number, create_xml, to_sent_to_sftp, get_server_address


def cp_contract_sign(purchase, send=True):
    """Подписанный контракт"""

    template = open_xml("templates/draft_contract/cpContractSign.xml")

    template.find('.//ns7:id', ns).text = random_number(8)
    template.find('.//ns7:purchaseNumber', ns).text = purchase.purchase_number
    template.find('.//ns7:purchaseCode', ns).text = purchase.purchase_code

    xml = create_xml(template)

    if send:
        to_sent_to_sftp(xml, purchase.server_address)
