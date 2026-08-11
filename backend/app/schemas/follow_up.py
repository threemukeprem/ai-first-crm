from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FollowUpBase(BaseModel):
    hcp_id: int = Field(gt=0)
    interaction_id: int | None = Field(default=None, gt=0)
    title: str = Field(min_length=2, max_length=200)
    description: str | None = None
    due_date: datetime
    status: str = Field(default="pending", min_length=2, max_length=30)


class FollowUpCreate(FollowUpBase):
    pass


class FollowUpUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=2, max_length=200)
    description: str | None = None
    due_date: datetime | None = None
    status: str | None = Field(default=None, min_length=2, max_length=30)


class FollowUpRead(FollowUpBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime