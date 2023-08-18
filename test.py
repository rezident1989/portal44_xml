from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml


# xml_1 = open_xml('outgoing/14433546_xml.xml')
# tag_list_1 = xml_1.find('.//ns3:position[1]/ns3:commonInfo/ns3:extNumber', ns)
# print(tag_list_1.text)
# print('ДОКУМЕНТ №1')
# print(f'Количество тегов: {len(tag_list_1)}')
# [print(i.text) for i in tag_list_1]

# print('-' * 40)
#
# xml_2 = open_xml('outgoing/14922532_xml.xml')
#
# tag_list_2 = xml_2.findall('.//ns2:execution/ns2:docExecution/..', ns)
# print(tag_list_2)
# print('ДОКУМЕНТ №2')
# print(f'Количество тегов: {len(tag_list_2)}')
# [print(i.text) for i in tag_list_2]
# #
# print('-' * 40)
#
# a = tag_list_2 = xml_2.find('.//ns2:docExecution[2]/ns2:externalSid', ns)
# print(a.text)

for a, b in enumerate([1, 3]):
    for c, d in enumerate([2, 4]):
        if a == c:
            print(b, d)
