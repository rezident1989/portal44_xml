import logging

from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml

# xml_1 = open_xml('incoming/12.43_15.08.23_tenderPlan2020.xml').getroot()
# tag_list_1 = xml_1.findall('.//ns3:specialPurchasePosition/ns3:extNumber', ns)
# print('ДОКУМЕНТ_1')
# print(f'Количество тегов: {len(tag_list_1)}')
# [print(i.text) for i in tag_list_1]

# print('-' * 40)
#
# xml_2 = open_xml('outgoing/15104665_xml.xml').getroot()
# tag_list_2 = xml_2.findall('.//ns3:specialPurchasePosition/ns3:extNumber', ns)
# print('ДОКУМЕНТ_2')
# print(f'Количество тегов: {len(tag_list_2)}')
# [print(i.text) for i in tag_list_2]

logging.getLogger('test')
logging.basicConfig(filename='test.log')
a = open_xml('outgoing/tenderPlan2020Change.xml')
logging.warning('test1')
# b = open_xml('outgoing/tenderPlan2020Change.xml').getroot()
count = 0
# for i in a.iter():
#     count += 1
# print(count)
# count = 0
# for i in b.iter():
#     count += 1
print(count)
