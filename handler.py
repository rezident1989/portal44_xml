from src.helper.help_func import clear_folder, get_type_xml, get_server_address, create_xml, to_sent_to_sftp
from src.helper.schema_xsd import validate_xsd
from src.actions.confirmation import confirmation
from src.actions.tender_plan import tender_plan_2020
from src.actions.notification import (ep_notification_ef_2020, ep_protocol_ef_2020_submit_offers,
                                      ep_protocol_ef_2020_final)
from src.actions.contract import contract

if __name__ == '__main__':
    path = 'outgoing/15104665_xml.xml'
    clear_folder('incoming')
    validate_xsd(path)
    server_address = get_server_address(path)
    type_xml = get_type_xml(path)

    path_confirmation = create_xml(confirmation(path))
    to_sent_to_sftp(path_confirmation, server_address)

    if ('tenderPlan2020' == type_xml) or ('tenderPlan2020Change' == type_xml):
        create_xml(tender_plan_2020(path))
        path_tender_plan_2020 = create_xml(tender_plan_2020(path))
        validate_xsd(path_tender_plan_2020)
        to_sent_to_sftp(path_tender_plan_2020, server_address)
    elif 'epNotificationEF2020' == type_xml:
        for func in [ep_notification_ef_2020, ep_protocol_ef_2020_submit_offers, ep_protocol_ef_2020_final]:
            path = create_xml(func(path))
            validate_xsd(path)
            # to_sent_to_sftp(path, server_address)
    elif 'contract' == type_xml:
        path_contract = create_xml(contract(path))
        validate_xsd(path_contract)
        # to_sent_to_sftp(path_contract, server_address)
    else:
        print('Нет обработки для:', type_xml)
