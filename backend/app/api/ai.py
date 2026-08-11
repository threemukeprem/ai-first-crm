from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.follow_up import FollowUp
from app.models.interaction import Interaction
from app.models.tool_audit_log import ToolAuditLog
from app.schemas.ai import (
    InteractionAnalysisRequest,
    InteractionAnalysisResponse,
    StoredInteractionAnalysisRequest,
    StoredInteractionAnalysisResponse,
)
from app.services.interaction_graph import analyze_with_graph

router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


class AIResult:
    def __init__(self, data: dict):
        self.summary = data["summary"]
        self.sentiment = data["sentiment"]
        self.suggested_follow_up = data["suggested_follow_up"]
        self.provider = data["provider"]


@router.post(
    "/analyze-interaction",
    response_model=InteractionAnalysisResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_interaction_endpoint(
    payload: InteractionAnalysisRequest,
    db: Session = Depends(get_db),
):
    try:
        graph_result = analyze_with_graph(payload.notes)
        result = AIResult(graph_result)

        audit_log = ToolAuditLog(
            tool_name="interaction_analyzer",
            tool_input=payload.notes,
            tool_output=(
                f"provider={result.provider}; "
                f"summary={result.summary}; "
                f"sentiment={result.sentiment}; "
                f"suggested_follow_up={result.suggested_follow_up}"
            ),
            status="success",
            error_message=None,
        )

        db.add(audit_log)
        db.commit()

        return InteractionAnalysisResponse(
            summary=result.summary,
            sentiment=result.sentiment,
            suggested_follow_up=result.suggested_follow_up,
            provider=result.provider,
        )

    except Exception as exc:
        db.rollback()

        failed_log = ToolAuditLog(
            tool_name="interaction_analyzer",
            tool_input=payload.notes,
            tool_output=None,
            status="failed",
            error_message=str(exc),
        )

        db.add(failed_log)
        db.commit()

        raise


@router.post(
    "/analyze-interaction/{interaction_id}",
    response_model=StoredInteractionAnalysisResponse,
    status_code=status.HTTP_200_OK,
)
def analyze_stored_interaction(
    interaction_id: int,
    payload: StoredInteractionAnalysisRequest,
    db: Session = Depends(get_db),
):
    interaction = db.get(Interaction, interaction_id)

    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found.",
        )

    try:
        graph_result = analyze_with_graph(interaction.notes)
        result = AIResult(graph_result)

        interaction.ai_summary = result.summary
        interaction.sentiment = result.sentiment

        follow_up = None

        if payload.create_follow_up:
            follow_up = FollowUp(
                hcp_id=interaction.hcp_id,
                interaction_id=interaction.id,
                title="AI Recommended Follow-up",
                description=result.suggested_follow_up,
                due_date=datetime.now() + timedelta(days=7),
                status="pending",
            )
            db.add(follow_up)

        audit_log = ToolAuditLog(
            tool_name="stored_interaction_analyzer",
            tool_input=interaction.notes,
            tool_output=(
                f"interaction_id={interaction.id}; "
                f"provider={result.provider}; "
                f"summary={result.summary}; "
                f"sentiment={result.sentiment}; "
                f"suggested_follow_up={result.suggested_follow_up}"
            ),
            status="success",
            error_message=None,
        )

        db.add(audit_log)

        db.commit()

        db.refresh(interaction)

        if follow_up is not None:
            db.refresh(follow_up)

        return StoredInteractionAnalysisResponse(
            interaction_id=interaction.id,
            ai_summary=interaction.ai_summary,
            sentiment=interaction.sentiment,
            suggested_follow_up=result.suggested_follow_up,
            provider=result.provider,
            follow_up_created=follow_up is not None,
            follow_up_id=follow_up.id if follow_up else None,
        )

    except Exception as exc:
        db.rollback()

        failed_log = ToolAuditLog(
            tool_name="stored_interaction_analyzer",
            tool_input=interaction.notes,
            tool_output=None,
            status="failed",
            error_message=str(exc),
        )

        db.add(failed_log)
        db.commit()

        raise