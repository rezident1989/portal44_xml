from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml
from src.helper.schema_xsd import validate_xsd
# xml_1 = open_xml('templates/contractProcedure.xml')
# tag_list_1 = xml_1.findall('.//ns2:execution/ns2:docAcceptance/..', ns)
# a = tag_list_1[0]
# print(a.find('.//ns2:sid', ns).text)
# print('ДОКУМЕНТ №1')
# print(f'Количество тегов: {len(tag_list_1)}')
# [print(i.text) for i in tag_list_1]
#
# print('-' * 40)
#
# xml_2 = open_xml('outgoing/15104701_xml (1).xml')
#
# tag_list_2 = xml_2.findall('.//ns2:execution/ns2:docAcceptance/..', ns)
# b = tag_list_2[0]
# print(b.find('.//ns2:sid', ns).text)
# print('ДОКУМЕНТ №2')
# print(f'Количество тегов: {len(tag_list_2)}')
# [print(i.text) for i in tag_list_2]

validate_xsd('outgoing/contract_21.08.1.xml')
