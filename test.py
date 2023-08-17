from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml


# xml_1 = open_xml('incoming/14.42_17.08.23_contractProcedure.xml')
# tag_list_1 = xml_1.findall('.//ns2:execution/ns2:payDoc', ns)
# print('ДОКУМЕНТ №1')
# print(f'Количество тегов: {len(tag_list_1)}')
# [print(i.text) for i in tag_list_1]

print('-' * 40)

xml_2 = open_xml('outgoing/14922514_xml.xml')
tag_list_2 = xml_2.findall('.//ns2:execution/ns2:docAcceptance', ns)
print('ДОКУМЕНТ №2')
print(f'Количество тегов: {len(tag_list_2)}')
[print(i.text) for i in tag_list_2]
