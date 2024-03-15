from enum import Enum


class RecordType(str, Enum):
    GENERATION = "generation"
    PRICE = "price"
    EVENT = "event"
    LAND_COVER = "land_cover"
    TECHNOLOGY_PARAMETER = "technology_parameter"
