from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml

xml_1 = open_xml('incoming/16.34_14.08.23_tenderPlan2020.xml').getroot()
tag_1 = './/ns3:specialPurchasePosition/ns3:publishYear'
tag_list_1 = xml_1.findall(xml_1, ns)
print('ДОКУМЕНТ_1')
print(f'Количество тегов: {len(tag_list_1)}')
[print(i.text) for i in tag_list_1]

xml_2 = open_xml('incoming/16.34_14.08.23_tenderPlan2020.xml').getroot()
tag_2 = './/ns3:specialPurchasePosition/ns3:publishYear'
tag_list_2 = xml_2.findall(xml_1, ns)
print('ДОКУМЕНТ_2')
print(f'Количество тегов: {len(tag_list_2)}')
[print(i.text) for i in tag_list_2]
