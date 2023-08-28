import ftplib
import os
from src.config.config_colorama import GREEN, RESET


def download_from_ftp(folder):
    ftp_host = 'ftp.zakupki.gov.ru'
    ftp_user = 'free'
    ftp_password = 'free'
    ftp = ftplib.FTP(ftp_host, ftp_user, ftp_password)
    ftp.cwd('fcs_regions/Sankt-Peterburg/contracts/currMonth')
    server_filenames = ftp.nlst()

    if not os.path.exists(os.path.join('..', folder)):
        os.makedirs(os.path.join('..', folder))

    for server_filename in server_filenames:
        full_name_file = os.path.join('..', folder, server_filename)
        if server_filename not in os.listdir(os.path.abspath(os.path.join('..', folder))):
            with open(full_name_file, 'wb') as f:
                ftp.retrbinary('RETR ' + server_filename, f.write)
                print(f'Архив {GREEN}{server_filename}{RESET} передан успешно')
    ftp.quit()


if __name__ == '__main__':
    download_from_ftp('ftp_1')
