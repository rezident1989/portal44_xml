from src.actions.confirm import confirm
from src.actions.tender_plan_2020 import tender_plan_2020

outgoing_xml = 'outgoing/15104596_xml.xml'

if __name__ == '__main__':
    confirm(outgoing_xml)
    tender_plan_2020(outgoing_xml)
