from enum import Enum


class OrderStatus(Enum):
    ordered = 'ordered'
    process = 'process'
    deliver = 'deliver'
    done = 'done'
    rejected = 'rejected'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]


class ObjectStatus(Enum):
    new = 'new'
    accepted = 'accepted'
    rejected = 'rejected'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]


class CharacteristicTitleLn(Enum):
    rang = 'rang'
    xotira = 'xotira'
    olcham = 'o\'lcham'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]


class CharacteristicTitleKr(Enum):
    ранг = 'ранг'
    хотира = 'хотира'
    ўлчам = 'ўлчам'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]


class CharacteristicTitleRu(Enum):
    цвет = 'цвет'
    память = 'память'
    размер = 'размер'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]


class CharacteristicTitleEn(Enum):
    color = 'color'
    memory = 'memory'
    size = 'size'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]
    

class ProductItemStatus(Enum):
    accepted = 'accepted'
    not_accepted = 'not_accepted'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]
    

class CompanyType(Enum):
    mchj = 'MCHJ'
    yatt = 'YATT'
    family_business = 'family_business'
    family_company = 'family_company'
    personal_business = 'personal_business'

    @classmethod
    def choices(cls):
        return [
            (key.value, key.name)
            for key in cls
        ]
