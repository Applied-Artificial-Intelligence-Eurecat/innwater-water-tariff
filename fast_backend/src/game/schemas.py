from pydantic import BaseModel

class RoundSchema(BaseModel):
    alpha: float
    ratio_tbse: float
    threshold_res: float

class RoundSchemaResponse(RoundSchema):
    round_id: int

class ParticipationSchema(BaseModel):
    round_id: int
    simulation_name: str
    score: float


class ParticipationRound(BaseModel):
    round_id: int
    alpha: float
    ratio_tbse: float
    threshold_res: float
    score: float