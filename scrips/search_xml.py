import os
import zipfile


def search_xml(text):
    count_res = 0
    byte_object = text.encode("utf-8")

    for i in os.listdir('../ftp_server'):
        if count_res != 0:
            break
        with zipfile.ZipFile(f"../ftp_server/{i}", "r") as myzip:
            for file_info in myzip.infolist():
                if file_info.filename.endswith('.xml'):
                    if byte_object in myzip.read(file_info):
                        count_res += 1
                        myzip.extract(file_info, os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop', 'xml'))


if __name__ == '__main__':
    search_xml('penalties')
