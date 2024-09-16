from dataclasses import dataclass


@dataclass
class Notification:

    schema_version: dict = None
    server_address: str = None
    purchase_number: str = None
    external_id: str = None
    version_number: str = None
    doc_number: str = None
    publish_in_eis: str = None
    stages: tuple = None
    purchase_objects: tuple = None
    drug_purchase_objects: tuple = None
    drugs: tuple = None
