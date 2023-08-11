import paramiko


# Open a transport
transport = paramiko.Transport('testaisgz3.gz-spb.ru')
transport.connect(None, username='root', password='12345678')
sftp = paramiko.SFTPClient.from_transport(transport)

# Go!
print(sftp.listdir('../OOC'))
# sftp.put('incoming/10.06_11.08.23_confirmation.xml', '../OOC/Incoming/tes4t.py')
# print(sftp.listdir('../OOC/Incoming'))

# Close a transport
if sftp:
    sftp.close()
if transport:
    transport.close()

# sftp.get('../OOC/Incoming/test.py', os.path.abspath('123.py'))
# a = 'incoming/12.17_10.08.23_confirmation.xml'
# b = a.split('/')[-1:][0]
# print(b)