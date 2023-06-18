from pydantic import BaseModel


class TechnologyParameter(BaseModel):
    code: str
    dispay_name: str
    value: float


class Technology(BaseModel):
    code: str
    display_name: str
    parameters: List[TechnologyParameter]
    capacity: float
