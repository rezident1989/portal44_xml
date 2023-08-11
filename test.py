from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml

outgoing_xml = open_xml('outgoing/14922461_xml.xml').getroot()
name_tag_outgoing = './/ns1:data/ns2:regNum'
outgoing = outgoing_xml.findall(name_tag_outgoing, ns)
print('ИСХОДЯЩИЙ')
print(f'Количество тегов "{name_tag_outgoing}" в исходящем файле: {len(outgoing)}')
[print(i.text) for i in outgoing]

incoming_xml = open_xml('templates/contract.xml').getroot()
name_tag_template = './/ns4:contract/ns2:regNum'
template = incoming_xml.findall(name_tag_template, ns)
print('Входящий')
print(f'Количество тегов "{name_tag_template}" в исходящем файле: {len(template)}')
[print(i.text) for i in template]



# template_xml = open_xml('templates/contract.xml').getroot()
# incoming_xml = open_xml('incoming/11.55_10.08.23_confirmation.xml').getroot()
#
# name_tag_template = './/ns4:contract/ns2:regNum'
#
# template = template_xml.findall(name_tag_template, ns)
# incoming = incoming_xml.findall(name_tag_template, ns)
# outgoing = outgoing_xml.findall(name_tag_outgoing, ns)
#
# print(f'Количество тегов "{name_tag_template}" в шаблоне: {len(template)}\n')
# [print(i.text) for i in template]
#
# print(f'Количество тегов "{name_tag_template}" в шаблоне: {len(incoming)}\n')
# [print(i.text) for i in incoming]
