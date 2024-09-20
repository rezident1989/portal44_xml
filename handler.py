import sys

from actions.confirmation import confirmation
from actions.contract.contract import contract
from actions.contract.contract_procedure import contract_procedure
from actions.draft_contract.cp_contract_sign import cp_contract_sign, cp_closed_contract_sign
from actions.draft_contract.cp_electronic_contract import cp_electronic_contract, cp_electronic_contract_eis
from actions.notification import notification
from actions.protocols.ef_2020 import ef_protocol_submit_offers, ef_protocol_final_part
from actions.protocols.ezk_2020 import ezk_closed_protocol_final
from actions.tender_plan import tender_plan_2020
from src.pickle_module import save_data, load_data
from src.system_functions import clear_folder, get_type_xml, validate_xsd, get_path_xml, remove_file


def handler(send=True):
    path = get_path_xml()
    clear_folder('incoming')

    validate_xsd(path)
    type_xml = get_type_xml(path)

    if type_xml == 'tenderPlan2020Change':
        tender_plan_2020(path, send)

    elif type_xml in ['epNotificationEF2020', 'epClosedInvitationEZakA2020']:
        confirmation(path, send)
        data = notification(path, type_xml, send)

        if type_xml == 'epNotificationEF2020':
            ef_protocol_submit_offers(data, send)
            ef_protocol_final_part(data, send)

        elif type_xml == 'epClosedInvitationEZakA2020':
            ezk_closed_protocol_final(data, send)

        save_data(data, 'purchase')

    elif type_xml == 'contract':
        confirmation(path, send)
        contract(path, send)

    elif type_xml == 'contractProcedure':
        confirmation(path, send)
        contract_procedure(path, send)

    elif type_xml in ['cpContractProject', 'cpClosedContractProject']:
        confirmation(path, send)
        pass

    elif '10_CpElectronicContract' in path:
        purchase = load_data('purchase')
        cp_electronic_contract_eis(purchase, send)

        if purchase.placing_way_cod == 'EAP20':
            cp_contract_sign(purchase, send)
        elif purchase.placing_way_cod == 'ZAP20':
            cp_closed_contract_sign(purchase, send)

    elif type_xml == 'cpElectronicContract':
        purchase = load_data('purchase')
        confirmation(path, send)
        cp_electronic_contract(path, send)

        if purchase.placing_way_cod == 'EAP20':
            cp_contract_sign(purchase, send)
        elif purchase.placing_way_cod == 'ZAP20':
            cp_closed_contract_sign(purchase, send)

    else:
        print('Нет обработки для пакета:', type_xml)
        sys.exit(1)

    remove_file(path, 'archive', send)
    print('Программа закончила обработку пакетов')


if __name__ == '__main__':
    handler(send=True)
