import sys
from src.helper.help_func import clear_folder, get_type_xml, get_server_address, create_xml, to_sent_to_sftp, \
    remove_file, test_folder, validate_xsd, get_path_xml
from actions.confirmation import confirmation
from actions.tander_plan.tender_plan import tender_plan_2020
from actions.notification.ef_2020 import ef_notification, ef_final_protocol
from actions.notification.ezt_2020 import ezt_notification, ezt_final_protocol
from actions.notification.eok_2020 import eok_sop
from actions.contract.contract import contract
from actions.contract.contract_procedure import contract_procedure


def handler(validation=True, send=True):
    path = get_path_xml()
    clear_folder('incoming')
    files = []
    files_to_send = []
    files_for_validation = []

    validate_xsd(path)
    server_address = get_server_address(path)
    type_xml = get_type_xml(path)
    print(path, 'this is', type_xml)

    files_to_send.extend(create_xml(confirmation(path)))   # Confirm

    if ('tenderPlan2020' == type_xml) or ('tenderPlan2020Change' == type_xml):  # Тендер-план
        files.extend(create_xml(tender_plan_2020(path)))
    elif 'epNotificationEF2020' == type_xml:  # Электронный аукцион
        files.extend(create_xml(ef_notification(path)))
        files.extend(create_xml(ef_final_protocol(path)))
    elif 'epNotificationEZT2020' == type_xml:  # "Закупка с полки" (или Закупка товаров согласно ч.12 ст. 93 № 44-ФЗ)
        files.extend(create_xml(ezt_notification(path)))
        files.extend(create_xml(ezt_final_protocol(path)))
    elif 'epNotificationEOK2020' == type_xml:  # Открытый конкурс в электронной форме
        files.extend(create_xml(eok_sop(path)))
    elif 'contract' == type_xml or 'closedContract' == type_xml:  # Контракт
        files.extend(create_xml(contract(path)))
    elif 'contractProcedure' == type_xml:  # Исполнение контракта
        files.extend(create_xml(contract_procedure(path)))
    else:
        print('Нет обработки для пакета:', type_xml)
        sys.exit(1)

    files_for_validation.extend(files)
    files_to_send.extend(files)

    if validation:
        for file in files_for_validation:
            validate_xsd(file)

    if send:
        for file in files_to_send:
            to_sent_to_sftp(file, server_address)

    remove_file(path, 'archive')
    test_folder(server_address)
