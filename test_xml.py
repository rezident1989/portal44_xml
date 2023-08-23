import ftplib

from src.helper.namespace import namespace as ns
from src.helper.help_func import open_xml, test_folder
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

# validate_xsd('outgoing/contract_21.08.1.xml')

import paramiko
from password import password_sftp

# transport = paramiko.Transport('testaisgz5.gz-spb.ru')
# transport.connect(None, username='root', password=password_sftp)
# sftp = paramiko.SFTPClient.from_transport(transport)
# a = len(sftp.listdir(f'../OOC/IncomingCog/123.xml'))
# print(a)
# # if host == 'testaisgz5.gz-spb.ru' or host == 'testaisgz4.gz-spb.ru':
# #     sftp.put(path, f'../OOC/IncomingCog/{path.split("/")[-1:][0]}')
# # else:
# #     sftp.put(path, f'../OOC/Incoming/{path.split("/")[-1:][0]}')
# # print(path.split("/")[-1:][0], 'отправлен на', host)
#
# if sftp:
#     sftp.close()
# if transport:
#     transport.close()


from ftplib import FTP
ftp_host = 'ftp.zakupki.gov.ru'
ftp_user = 'free'
ftp_password = 'free'
ftp = ftplib.FTP(ftp_host, ftp_user, ftp_password)
print(ftp.nlst('fcs_regions/Sankt-Peterburg/'))
directory = ftp.cwd('fcs_regions/Sankt-Peterburg/plangraphs2020/prevMonth/')


print(directory)
ftp.quit()
