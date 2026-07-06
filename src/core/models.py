from datetime import datetime
from uuid import UUID, uuid4

from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Coordinate

from core.cot.choices import Affiliation, CotType


class TargetPos(BaseModel):
    coords: Coordinate
    description: str
    timestamp: int
    affiliation: Affiliation = Affiliation.UNKNOWN


class CursorOnTarget(BaseModel):
    coords: Coordinate
    description: str
    uid: UUID = Field(default_factory=uuid4)
    how: str = "m-g" 
    type: CotType
    time: datetime
    start: datetime
    stale: datetime
    affiliation: Affiliation

