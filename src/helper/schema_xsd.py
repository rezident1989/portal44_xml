import sys
from lxml import etree


def validate_xsd(path):
    # Загрузка xsd схемы
    if 'outgoing' in path:
        schema_path = r'src/schemes/fcsIntegration.xsd'
    else:
        schema_path = r'src/schemes/fcsExport.xsd'

    path_xsd = etree.parse(schema_path)
    schema = etree.XMLSchema(path_xsd)

    # Загрузка xml
    xml = etree.parse(path)
    a = path.split('/')[1]
    b = schema_path.split('/')[2]

    # Проверка
    if not schema.validate(xml):
        print(schema.error_log)
        sys.exit(1)
    else:
        print(f'{a} соответствует схеме {b}')
