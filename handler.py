from src.helper.help_func import open_xml
from src.helper.schema_xsd import validate_xsd
from src.actions.confirmation import confirmation
from src.actions.tender_plan import tender_plan_2020
import src.actions.notification as notification
from src.actions.contract import contract

if __name__ == '__main__':
    path_xml = 'outgoing/14433512_xml 07.08.xml'
    validate_xsd(path_xml)
    root_tag = open_xml(path_xml).getroot().tag

    confirmation(path_xml)
    if 'tenderPlan2020' in root_tag:
        tender_plan_2020(path_xml)
    elif 'epNotificationEF2020' in root_tag:
        notification.ep_notification_ef_2020(path_xml)
        notification.ep_protocol_ef_2020_submit_offers(path_xml)
        notification.ep_protocol_ef_2020_final(path_xml)
    elif 'contract' in root_tag:
        contract(path_xml)
