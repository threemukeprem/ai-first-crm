from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.tool_audit_log import ToolAuditLog
from app.schemas.tool_audit_log import (
    ToolAuditLogCreate,
    ToolAuditLogRead,
)


router = APIRouter(
    prefix="/tool-audit-logs",
    tags=["Tool Audit Logs"],
)


@router.post(
    "",
    response_model=ToolAuditLogRead,
    status_code=status.HTTP_201_CREATED,
)
def create_tool_audit_log(
    payload: ToolAuditLogCreate,
    db: Session = Depends(get_db),
) -> ToolAuditLog:
    audit_log = ToolAuditLog(**payload.model_dump())

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log


@router.get(
    "",
    response_model=list[ToolAuditLogRead],
)
def list_tool_audit_logs(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[ToolAuditLog]:
    statement = (
        select(ToolAuditLog)
        .order_by(ToolAuditLog.created_at.desc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{audit_log_id}",
    response_model=ToolAuditLogRead,
)
def get_tool_audit_log(
    audit_log_id: int,
    db: Session = Depends(get_db),
) -> ToolAuditLog:
    audit_log = db.get(ToolAuditLog, audit_log_id)

    if audit_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tool audit log not found.",
        )

    return audit_log