from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ToolAuditLogBase(BaseModel):
    thread_id: str | None = Field(default=None, max_length=100)
    tool_name: str = Field(min_length=1, max_length=100)
    tool_input: str | None = None
    tool_output: str | None = None
    status: str = Field(min_length=1, max_length=30)
    error_message: str | None = None


class ToolAuditLogCreate(ToolAuditLogBase):
    pass


class ToolAuditLogRead(ToolAuditLogBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime