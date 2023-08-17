from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml


xml_1 = open_xml('templates/contractProcedure.xml')
tag_list_1 = xml_1.findall('.//ns2:execution/ns2:docExecution/ns2:externalSid', ns)
print('ДОКУМЕНТ №1')
print(f'Количество тегов: {len(tag_list_1)}')
[print(i.text) for i in tag_list_1]

print('-' * 40)

xml_2 = open_xml('outgoing/14922507_xml.xml')
tag_list_2 = tag_list_1
print('ДОКУМЕНТ №2')
print(f'Количество тегов: {len(tag_list_2)}')
[print(i.text) for i in tag_list_2]



