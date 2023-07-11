from src.actions.confirnation import confirmation
from src.actions.tender_plan_2020 import tender_plan_2020

outgoing_xml = 'outgoing/14433458_xml.xml'

if __name__ == '__main__':
    confirmation(outgoing_xml)
    tender_plan_2020(outgoing_xml)
