from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hcp import HCP
from app.models.interaction import Interaction
from app.schemas.interaction import (
    InteractionCreate,
    InteractionRead,
    InteractionUpdate,
)


router = APIRouter(
    prefix="/interactions",
    tags=["Interactions"],
)


@router.post(
    "",
    response_model=InteractionRead,
    status_code=status.HTTP_201_CREATED,
)
def create_interaction(
    payload: InteractionCreate,
    db: Session = Depends(get_db),
) -> Interaction:
    hcp = db.get(HCP, payload.hcp_id)

    if hcp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found.",
        )

    interaction = Interaction(**payload.model_dump())

    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    return interaction


@router.get(
    "",
    response_model=list[InteractionRead],
)
def list_interactions(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[Interaction]:
    statement = (
        select(Interaction)
        .order_by(Interaction.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{interaction_id}",
    response_model=InteractionRead,
)
def get_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
) -> Interaction:
    interaction = db.get(Interaction, interaction_id)

    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found.",
        )

    return interaction


@router.patch(
    "/{interaction_id}",
    response_model=InteractionRead,
)
def update_interaction(
    interaction_id: int,
    payload: InteractionUpdate,
    db: Session = Depends(get_db),
) -> Interaction:
    interaction = db.get(Interaction, interaction_id)

    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(interaction, field, value)

    db.commit()
    db.refresh(interaction)

    return interaction


@router.delete(
    "/{interaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_interaction(
    interaction_id: int,
    db: Session = Depends(get_db),
) -> None:
    interaction = db.get(Interaction, interaction_id)

    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interaction not found.",
        )

    db.delete(interaction)
    db.commit()