import sys

from actions.confirmation import confirmation
from actions.contract.contract import contract
from actions.contract.contract_procedure import contract_procedure
from actions.notification.ef_2020 import ef_notification, ef_final_protocol, ef_submit_offers
from actions.notification.eok_2020 import eok_sop
from actions.notification.ezt_2020 import ezt_notification, ezt_final_protocol
from actions.tender_plan import tender_plan_2020
from src.system_functions import clear_folder, get_type_xml, validate_xsd, get_path_xml


def handler():
    path = get_path_xml()
    clear_folder('incoming')

    validate_xsd(path)
    type_xml = get_type_xml(path)
    print(type_xml)

    if type_xml == 'tenderPlan2020Change':  # Тендер-план
        tender_plan_2020(path)
    elif type_xml == 'epNotificationEF2020':  # Электронный аукцион
        confirmation(path)
        data = ef_notification(path)
        ef_submit_offers(path, data)
        ef_final_protocol(path, data)
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
