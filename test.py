import xml.etree.ElementTree as ET
import copy
from src.helper.namespace import namespace as ns
from src.helper.help_func import create_xml, open_xml


tree = open_xml('templates/tenderPlan2020.xml')
root = tree.getroot()
# Find element to copy
member1 = tree.find(".//ns3:specialPurchasePosition", ns)
# Create a copy
member2 = copy.deepcopy(member1)
# Append the copy
member3 = tree.find(".//ns3:specialPurchasePositions", ns)
print(len(tree.findall(".//ns3:specialPurchasePosition", ns)))
member3.append(member2)
member4 = root[0]
print(member4)

member4.remove(member3)
create_xml(tree)

print(len(tree.findall(".//ns3:specialPurchasePosition", ns)))