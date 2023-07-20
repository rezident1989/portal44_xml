from src.helper.help_func import open_xml
from src.actions.confirmation import confirmation
from src.actions.tender_plan import tender_plan_2020
from src.actions.notification import ep_notification_ef_2020_final
from src.actions.contract import contract

if __name__ == '__main__':
    path_xml = 'outgoing/14433489_xml_извещение_Пониделко.xml'
    file_xml = open_xml(path_xml)

    if 'epNotificationEF2020' in file_xml.getroot().tag:
        confirmation(path_xml)
        ep_notification_ef_2020_final(path_xml)
    elif 'tenderPlan2020' in file_xml.getroot().tag:
        confirmation(path_xml)
        tender_plan_2020(path_xml)
    elif 'contract' in file_xml.getroot().tag:
        confirmation(path_xml)
        contract(path_xml)
    else:
        confirmation(path_xml)
