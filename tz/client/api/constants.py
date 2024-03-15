from enum import Enum

COMMODITIES = ["ELEC"]


class ChartType(str, Enum):
    AGGREGATE_CAPACITY_BAR: str = "AggregateCapacityBar"
    FACETTED_PRODUCTION: str = "FacettedProduction"
    AGGREGATE_PRODUCTION_BAR: str = "AggregateProductionBar"
    CAPACITY: str = "Capacity"
    PRODUCTION: str = "Production"
    FLOW: str = "Flow"


CHART_TYPES = [item.value for item in ChartType]


class TechnologyType(str, Enum):
    BAT: str = "Battery"
    BIO: str = "Biomass"
    CCG: str = "Combined Cycle Gas"
    CCS: str = "Carbon Capture and Storage"
    COA: str = "Coal"
    COG: str = "Combined Cycle Gas"
    CSP: str = "Concentrated Solar Power"
    HYD: str = "Hydro"
    OCG: str = "Open Cycle Gas"
    OIL: str = "Oil"
    OTH: str = "Other"
    PET: str = "Petroleum"
    SPV: str = "Solar Photovoltaic"
    URN: str = "Uranium"
    WAS: str = "Waste"
    WOF: str = "Wind Offshore"
    WON: str = "Wind Onshore"


TECHOLOGY_TYPES = [item.value for item in TechnologyType]
TECHNOLOGY_MAP = {item.value: item for item in TechnologyType}
