from dataclasses import dataclass


@dataclass
class Notification:

    def __init__(self, purchase_number, server_address):
        self.purchase_number = purchase_number
        self.server_address = server_address

    schedule_period: str = '2024-2026 год'
