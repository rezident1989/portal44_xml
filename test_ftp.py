import ftplib


ftp_host = 'ftp.zakupki.gov.ru'
ftp_user = 'free'
ftp_password = 'free'
ftp = ftplib.FTP(ftp_host, ftp_user, ftp_password)
directory = ftp.nlst('fcs_regions/Sankt-Peterburg/')

print(directory)
ftp.quit()
