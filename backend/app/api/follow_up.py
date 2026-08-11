from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.follow_up import FollowUp
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.schemas.follow_up import (
    FollowUpCreate,
    FollowUpRead,
    FollowUpUpdate,
)


router = APIRouter(
    prefix="/follow-ups",
    tags=["Follow-Ups"],
)


@router.post(
    "",
    response_model=FollowUpRead,
    status_code=status.HTTP_201_CREATED,
)
def create_follow_up(
    payload: FollowUpCreate,
    db: Session = Depends(get_db),
) -> FollowUp:
    hcp = db.get(HCP, payload.hcp_id)

    if hcp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found.",
        )

    if payload.interaction_id is not None:
        interaction = db.get(Interaction, payload.interaction_id)

        if interaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Interaction not found.",
            )

        if interaction.hcp_id != payload.hcp_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Interaction does not belong to the specified HCP.",
            )

    follow_up = FollowUp(**payload.model_dump())

    db.add(follow_up)
    db.commit()
    db.refresh(follow_up)

    return follow_up


@router.get(
    "",
    response_model=list[FollowUpRead],
)
def list_follow_ups(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[FollowUp]:
    statement = (
        select(FollowUp)
        .order_by(FollowUp.due_date.asc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{follow_up_id}",
    response_model=FollowUpRead,
)
def get_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
) -> FollowUp:
    follow_up = db.get(FollowUp, follow_up_id)

    if follow_up is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow-up not found.",
        )

    return follow_up


@router.patch(
    "/{follow_up_id}",
    response_model=FollowUpRead,
)
def update_follow_up(
    follow_up_id: int,
    payload: FollowUpUpdate,
    db: Session = Depends(get_db),
) -> FollowUp:
    follow_up = db.get(FollowUp, follow_up_id)

    if follow_up is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow-up not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(follow_up, field, value)

    db.commit()
    db.refresh(follow_up)

    return follow_up


@router.delete(
    "/{follow_up_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_follow_up(
    follow_up_id: int,
    db: Session = Depends(get_db),
) -> None:
    follow_up = db.get(FollowUp, follow_up_id)

    if follow_up is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Follow-up not found.",
        )

    db.delete(follow_up)
    db.commit()