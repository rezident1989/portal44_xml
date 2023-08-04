from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml


template_xml = open_xml('templates/contract.xml')
outgoing_xml = open_xml('outgoing/14433491_xml.xml')

name_tag = './/ns4:contract/ns2:regNum'
template = template_xml.findall(name_tag, ns)
outgoing = outgoing_xml.findall(name_tag, ns)

print(f'Количество тегов "{name_tag}" в шаблоне: {len(template)}\n')
[print(i) for i in template]

print(f'Количество тегов "{name_tag}" в исходящем файле: {len(template)}\n')
[print(i) for i in outgoing]
