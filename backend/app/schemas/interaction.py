from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InteractionBase(BaseModel):
    hcp_id: int = Field(gt=0)
    interaction_type: str = Field(min_length=2, max_length=50)
    channel: str = Field(min_length=2, max_length=50)
    interaction_date: datetime
    notes: str = Field(min_length=1)

    ai_summary: str | None = None
    sentiment: str | None = Field(default=None, max_length=50)
    products_discussed: str | None = None
    topics_discussed: str | None = None
    objections: str | None = None
    outcome: str | None = None


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    interaction_type: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    channel: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
    )
    interaction_date: datetime | None = None
    notes: str | None = Field(default=None, min_length=1)
    ai_summary: str | None = None
    sentiment: str | None = Field(default=None, max_length=50)
    products_discussed: str | None = None
    topics_discussed: str | None = None
    objections: str | None = None
    outcome: str | None = None


class InteractionRead(InteractionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime