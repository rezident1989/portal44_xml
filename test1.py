import os

import paramiko

# client = paramiko.SSHClient
# client.set_missing_host_key_policy(paramiko.AutoAddPolicy(hostname='testaisgz3.gz-spb.ru))
# client.connect(hostname='testaisgz3.gz-spb.ru',
#                username='root',
#                password='12345678',
#                allow_agent=False,
#                look_for_keys=False)
#
# sftp = client.open_sftp()

import paramiko

paramiko.util.log_to_file("paramiko.log")

# Open a transport
host, port = "testaisgz3.gz-spb.ru", 22
transport = paramiko.Transport((host, port))

# Auth
username, password = "root", "12345678"
transport.connect(None, username, password)

# Go!
sftp = paramiko.SFTPClient.from_transport(transport)
print(sftp.listdir('../OOC/Incoming'))
file = os.path.abspath('test1.py')

sftp.get('../OOC/Incoming/test.py', os.path.abspath('123.py'))
# sftp.put('test.py', '../OOC/Incoming/test.py')

if sftp: sftp.close()
if transport: transport.close()
