import sys

from actions.confirmation import confirmation
from actions.contract.contract import contract
from actions.contract.contract_procedure import contract_procedure
from actions.notification.ef_2020 import ef_notification, ef_submit_offers, ef_final_part_protocol
from actions.tender_plan import tender_plan_2020
from src.system_functions import clear_folder, get_type_xml, validate_xsd, get_path_xml


def handler():
    path = get_path_xml()
    clear_folder('incoming')

    validate_xsd(path)
    type_xml = get_type_xml(path)

    if type_xml == 'tenderPlan2020Change':  # Тендер-план
        tender_plan_2020(path)
    elif type_xml == 'epNotificationEF2020':  # Электронный аукцион
        confirmation(path, send=False)
        data = ef_notification(path, send=False)
        ef_submit_offers(data, send=False)
        ef_final_part_protocol(data, send=False)
    # elif type_xml == 'epNotificationEZT2020':  # "Закупка с полки" (или Закупка товаров согласно ч.12 ст. 93 № 44-ФЗ)
    #     confirmation(path)
    #     ezt_notification(path)
    #     ezt_final_protocol(path)
    # elif type_xml == 'epNotificationEOK2020':  # Открытый конкурс в электронной форме
    #     confirmation(path)
    #     eok_sop(path)
    elif type_xml == 'contract' or type_xml == 'closedContract':  # Контракт
        confirmation(path)
        contract(path)
    elif type_xml == 'contractProcedure':  # Исполнение контракта
        confirmation(path)
        contract_procedure(path)
    elif type_xml == 'cpContractProject':  # Проект контракта
        confirmation(path)
    elif type_xml == 'cpElectronicContract':  # Электронный контракт
        confirmation(path)
    else:
        print('Нет обработки для пакета:', type_xml)
        sys.exit(1)

    # remove_file(path, 'archive')
    print('Программа закончила обработку пакетов')


if __name__ == '__main__':
    handler()
