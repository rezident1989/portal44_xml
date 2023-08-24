import ftplib
import os
from src.config.config_colorama import GREEN, RESET

ftp_host = 'ftp.zakupki.gov.ru'
ftp_user = 'free'
ftp_password = 'free'
ftp = ftplib.FTP(ftp_host, ftp_user, ftp_password)
ftp.cwd('fcs_regions/Sankt-Peterburg/contracts/currMonth')
server_filenames = ftp.nlst()

if not os.path.exists(os.path.join('..', 'ftp_server')):
    os.makedirs(os.path.join('..', 'ftp_server'))


for server_filename in server_filenames:
    full_name_file = os.path.join('..', 'ftp_server', server_filename)
    if server_filename not in os.listdir(os.path.abspath(os.path.join('../src', '..', 'ftp_server'))):
        with open(full_name_file, 'wb') as f:
            ftp.retrbinary('RETR ' + server_filename, f.write)
            print(f'Архив {GREEN}{server_filename}{RESET} передан успешно')
ftp.quit()
