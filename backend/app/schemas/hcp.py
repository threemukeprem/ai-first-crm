from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class HCPBase(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    specialty: str = Field(min_length=2, max_length=100)
    organization: str | None = Field(default=None, max_length=200)
    city: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    preferred_channel: str | None = Field(default=None, max_length=50)
    notes: str | None = None


class HCPCreate(HCPBase):
    pass


class HCPUpdate(BaseModel):
    full_name: str | None = Field(default=None, min_length=2, max_length=150)
    specialty: str | None = Field(default=None, min_length=2, max_length=100)
    organization: str | None = Field(default=None, max_length=200)
    city: str | None = Field(default=None, max_length=100)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=30)
    preferred_channel: str | None = Field(default=None, max_length=50)
    notes: str | None = None


class HCPRead(HCPBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime