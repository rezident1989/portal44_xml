from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml


template_xml = open_xml('templates/epProtocolEF2020SubmitOffers.xml')
outgoing_xml = open_xml('outgoing/14433504_xml извещение ЭА.xml')

template = template_xml.findall('.//ns5:commonInfo/ns5:purchaseNumber', ns)
outgoing = outgoing_xml.findall('.//ns5:commonInfo/ns5:purchaseNumber', ns)

print(len(template))
print(len(outgoing))
print()
[print(i) for i in template]
print()
[print(i) for i in outgoing]

