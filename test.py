from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml


# template_xml = open_xml('templates/contract.xml')
# outgoing_xml = open_xml('outgoing/14433491_xml.xml')
#
# template = template_xml.findall('.//ns4:contract/ns2:regNum', ns)
# outgoing = outgoing_xml.findall('.//ns1:data/ns2:regNum', ns)

print(len(template))
print(len(outgoing))
print()
[print(i) for i in template]
print()
[print(i) for i in outgoing]

print('ПРивте Амалия')
print('Alex1')