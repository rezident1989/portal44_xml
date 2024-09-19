import sys

from actions.confirmation import confirmation
from actions.contract.contract import contract
from actions.contract.contract_procedure import contract_procedure
from actions.draft_contract.cp_contract_sign import cp_contract_sign
from actions.draft_contract.cp_electronic_contract import cp_electronic_contract, cp_electronic_contract_eis
from actions.notification.ef_2020 import ef_notification, ef_submit_offers, ef_final_part_protocol
from actions.tender_plan import tender_plan_2020
from src.pickle_module import save_data, load_data
from src.system_functions import clear_folder, get_type_xml, validate_xsd, get_path_xml, remove_file


def handler(send=True):
    path = get_path_xml()
    clear_folder('incoming')

    validate_xsd(path)
    type_xml = get_type_xml(path)

    if type_xml == 'tenderPlan2020Change':
        tender_plan_2020(path, send)  # План-график закупок с 01.01.2020

    elif type_xml == 'epNotificationEF2020':
        confirmation(path, send)  # Пакет данных: Уведомление о результатах обработки информационного пакета
        data = ef_notification(path, send)  # Извещение о проведении ЭА20
        ef_submit_offers(data, send)  # Протокол подачи ценовых предложений ЭА20
        ef_final_part_protocol(data, send)  # Протокол подведения итогов определения поставщика
        save_data(data, 'purchase')

    elif type_xml == 'contract':
        confirmation(path, send)
        contract(path, send)  # Информация (проект информации) о заключенном контракте

    elif type_xml == 'contractProcedure':
        confirmation(path, send)
        contract_procedure(path, send)  # Информация об исполнении (расторжении) контракта

    elif type_xml == 'cpContractProject':
        confirmation(path, send)  # Пакет данных: Уведомление о результатах обработки информационного пакета

    elif '10_CpElectronicContract' in path:
        purchase = load_data('purchase')
        cp_electronic_contract_eis(purchase, send)  # Электронный контракт ЕИС
        cp_contract_sign(purchase, send)  # Подписанный контракт

    elif type_xml == 'cpElectronicContract':
        purchase = load_data('purchase')
        confirmation(path, send)
        cp_electronic_contract(path, send)  # Электронный контракт
        cp_contract_sign(purchase, send)  # Подписанный контракт

    else:
        print('Нет обработки для пакета:', type_xml)
        sys.exit(1)

    remove_file(path, 'archive', send)
    print('Программа закончила обработку пакетов')


if __name__ == '__main__':
    handler(send=True)
