from dataclasses import dataclass


@dataclass
class Purchase:

    schema_version: dict = None
    server_address: str = None
    purchase_number: str = None
    purchase_code: str = None
    external_id: str = None
    version_number: str = None
    doc_number: str = None
    publish_in_eis: str = None
    stages: tuple = None

    purchase_objects_sid: tuple = None
    purchase_objects_external_sid: tuple = None

    drug_purchase_objects_sid: tuple = None
    drug_external_sid: tuple = None
    drugs: tuple = None

    purchase_protocol_sid: tuple = None
    drug_protocol_sid: tuple = None
