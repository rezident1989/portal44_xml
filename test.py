from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml
from datetime import datetime, timezone
import datetime

template_xml = open_xml('templates/epNotificationEF.xml')
outgoing_xml = open_xml('outgoing/14433489_xml_извещение Пониделко.xml')

template = template_xml.findall('.//ns5:publishDTInEIS', ns)
outgoing = outgoing_xml.findall('.//ns5:publishDTInEIS', ns)

print(len(template))
print(len(outgoing))
#
# dt_now = datetime.now().isoformat()[:-3]
# a = datetime.now().strftime('%z')
# print(type(a))
#

now = datetime.datetime.now()
tz = timezone(datetime.timedelta(hours=-6), name="CST")
now_tz = now.replace(tzinfo=tz)
now_tz.isoformat("#","milliseconds")
print(tz)