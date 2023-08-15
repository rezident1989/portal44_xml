from src.helper.help_func import clear_folder, get_type_xml
from src.helper.schema_xsd import validate_xsd
from src.actions.confirmation import confirmation
from src.actions.tender_plan import tender_plan_2020
import src.actions.notification as notification
from src.actions.contract import contract

if __name__ == '__main__':
    clear_folder('incoming')
    path_xml = 'outgoing/15104667_xml.xml'
    validate_xsd(path_xml)
    root_tag = get_type_xml(path_xml)

    confirmation(path_xml)
    if ('tenderPlan2020' == root_tag) or ('tenderPlan2020Change' == root_tag):
        tender_plan_2020(path_xml)
    elif 'epNotificationEF2020' == root_tag:
        notification.ep_notification_ef_2020(path_xml)
        notification.ep_protocol_ef_2020_submit_offers(path_xml)
        notification.ep_protocol_ef_2020_final(path_xml)
    elif 'contract' == root_tag:
        contract(path_xml)
    else:
        print('Нет обработки для:', root_tag)
