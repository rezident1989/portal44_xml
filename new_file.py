import xml.etree.ElementTree as ET

test = list()
count = 0

tree = ET.ElementTree(file='xml.xml')
for i in tree.iter():
    count += 1
    test.append(i.text.replace('\n', '').replace('  ', ' '))

print(count)
