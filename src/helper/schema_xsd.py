from lxml import etree


def validate_xsd(path_xml):
    # Загрузка xsd схемы
    if 'outgoing' in path_xml:
        schema_path = r'src/schemes/fcsIntegration.xsd'
    else:
        schema_path = r'src/schemes/fcsExport.xsd'

    path_xsd = etree.parse(schema_path)
    schema = etree.XMLSchema(path_xsd)

    # Загрузка xml
    xml = etree.parse(path_xml)
    a = path_xml.split('/')[1]
    b = schema_path.split('/')[2]

    # Проверка
    if not schema.validate(xml):
        print(schema.error_log)
    else:
        print(f'{a} соответствует схеме {b}')
