from pydantic import BaseModel, Field


class InteractionAnalysisRequest(BaseModel):
    notes: str = Field(min_length=1)

class StoredInteractionAnalysisRequest(BaseModel):
    create_follow_up: bool = False


class InteractionAnalysisResponse(BaseModel):
    summary: str
    sentiment: str
    suggested_follow_up: str
    provider: str

class StoredInteractionAnalysisResponse(BaseModel):
    interaction_id: int
    ai_summary: str
    sentiment: str
    suggested_follow_up: str
    provider: str
    follow_up_created: bool
    follow_up_id: int | None