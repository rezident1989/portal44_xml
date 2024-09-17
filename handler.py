import sys

from actions.confirmation import confirmation
from actions.contract.contract import contract
from actions.contract.contract_procedure import contract_procedure
from actions.draft_contract.cp_contract_sign import cp_contract_sign
from actions.draft_contract.cp_electronic_contract import cp_electronic_contract
from actions.notification.ef_2020 import ef_notification, ef_submit_offers, ef_final_part_protocol
from actions.tender_plan import tender_plan_2020
from src.system_functions import clear_folder, get_type_xml, validate_xsd, get_path_xml, remove_file


def handler():
    path = get_path_xml()
    clear_folder('incoming')

    validate_xsd(path)
    type_xml = get_type_xml(path)

    if type_xml == 'tenderPlan2020Change':
        tender_plan_2020(path)  # План-график закупок с 01.01.2020

    elif type_xml == 'epNotificationEF2020':
        confirmation(path)  # Пакет данных: Уведомление о результатах обработки информационного пакета
        data = ef_notification(path)  # Извещение о проведении ЭА20
        ef_submit_offers(data)  # Протокол подачи ценовых предложений ЭА20
        ef_final_part_protocol(data)  # Протокол подведения итогов определения поставщика

    elif type_xml == 'contract':
        confirmation(path)
        contract(path)  # Информация (проект информации) о заключенном контракте

    elif type_xml == 'contractProcedure':
        confirmation(path)
        contract_procedure(path)  # Информация об исполнении (расторжении) контракта

    elif type_xml == 'cpContractProject':
        confirmation(path)  # Пакет данных: Уведомление о результатах обработки информационного пакета

    elif type_xml == 'cpElectronicContract':
        cp_electronic_contract(path)  # Электронный контракт
        cp_contract_sign(path)  # Подписанный контракт

    else:
        print('Нет обработки для пакета:', type_xml)
        sys.exit(1)

    remove_file(path, 'archive')
    print('Программа закончила обработку пакетов')


if __name__ == '__main__':
    handler()
