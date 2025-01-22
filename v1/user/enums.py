from enum import Enum


class UserRole(Enum):
    admin = 'admin'
    client = 'client'
    seller = 'seller'

    @classmethod
    def choices(cls):
        return (
            (key.value, key.name)
            for key in cls
        )
