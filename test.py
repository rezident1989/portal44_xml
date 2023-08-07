from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml


template_xml = open_xml('templates/confirmation.xml')

a = template_xml.getroot()
print(a.tag)
outgoing_xml = open_xml('outgoing/14433512_xml 07.08.xml')

name_tag = './/ns2:protocolDate'
template = template_xml.findall(name_tag, ns)
outgoing = outgoing_xml.findall(name_tag, ns)

print(f'Количество тегов "{name_tag}" в шаблоне: {len(template)}\n')
[print(i) for i in template]

print(f'Количество тегов "{name_tag}" в исходящем файле: {len(template)}\n')
[print(i) for i in outgoing]

print('test v.1')
print('test v.2')
print('test v.3')
print('test v.4')


import secrets
print(secrets.token_hex(32))

a = "2780804311155801217"

print(len(a))