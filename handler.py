from src.helper.help_func import clear_folder, get_type_xml, get_server_address, create_xml, to_sent_to_sftp
from src.helper.schema_xsd import validate_xsd
from src.actions.confirmation import confirmation
from src.actions.tender_plan import tender_plan_2020
from src.actions.notification import (ep_notification_ef_2020, ep_protocol_ef_2020_submit_offers,
                                      ep_protocol_ef_2020_final)
from src.actions.contract import contract


def main(path, validation=True, send=True):
    clear_folder('incoming')
    files = None
    files_to_send = []
    files_for_validation = []
    validate_xsd(path)
    server_address = get_server_address(path)
    type_xml = get_type_xml(path)
    print(path, 'this is', type_xml)

    files_to_send.extend([create_xml(confirmation(path))])

    if ('tenderPlan2020' == type_xml) or ('tenderPlan2020Change' == type_xml):
        files = [create_xml(tender_plan_2020(path))]
    elif 'epNotificationEF2020' == type_xml:
        functions = [ep_notification_ef_2020, ep_protocol_ef_2020_submit_offers, ep_protocol_ef_2020_final]
        files = [create_xml(func(path)) for func in functions]
    elif 'contract' == type_xml:
        files = create_xml(contract(path))
    else:
        print('Нет обработки для:', type_xml)

    files_to_send.extend(files)
    files_for_validation.extend(files)

    if validation:
        for file in files_for_validation:
            validate_xsd(file)

    if send:
        for file in files_to_send:
            to_sent_to_sftp(file, server_address)


if __name__ == '__main__':
    main('outgoing/15104667_xml.xml')
