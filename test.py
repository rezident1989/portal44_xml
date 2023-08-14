from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml

xml_1 = open_xml('incoming/17.53_14.08.23_tenderPlan2020.xml').getroot()
tag_list_1 = xml_1.findall('.//ns3:specialPurchasePosition/ns3:publishYear', ns)
print('ДОКУМЕНТ_1')
print(f'Количество тегов: {len(tag_list_1)}')
[print(i.text) for i in tag_list_1]

print('-' * 40)

xml_2 = open_xml('templates/tenderPlan2020.xml').getroot()
tag_list_2 = xml_2.findall('.//ns3:specialPurchasePosition/ns3:publishYear', ns)
print('ДОКУМЕНТ_2')
print(f'Количество тегов: {len(tag_list_2)}')
[print(i.text) for i in tag_list_2]
