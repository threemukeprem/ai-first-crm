from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPRead, HCPUpdate


router = APIRouter(
    prefix="/hcps",
    tags=["HCPs"],
)


@router.post(
    "",
    response_model=HCPRead,
    status_code=status.HTTP_201_CREATED,
)
def create_hcp(
    payload: HCPCreate,
    db: Session = Depends(get_db),
) -> HCP:
    hcp = HCP(**payload.model_dump())

    db.add(hcp)

    try:
        db.commit()
        db.refresh(hcp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An HCP with this email already exists.",
        )

    return hcp


@router.get(
    "",
    response_model=list[HCPRead],
)
def list_hcps(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[HCP]:
    statement = (
        select(HCP)
        .order_by(HCP.id)
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


@router.get(
    "/{hcp_id}",
    response_model=HCPRead,
)
def get_hcp(
    hcp_id: int,
    db: Session = Depends(get_db),
) -> HCP:
    hcp = db.get(HCP, hcp_id)

    if hcp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found.",
        )

    return hcp


@router.patch(
    "/{hcp_id}",
    response_model=HCPRead,
)
def update_hcp(
    hcp_id: int,
    payload: HCPUpdate,
    db: Session = Depends(get_db),
) -> HCP:
    hcp = db.get(HCP, hcp_id)

    if hcp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found.",
        )

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(hcp, field, value)

    try:
        db.commit()
        db.refresh(hcp)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An HCP with this email already exists.",
        )

    return hcp


@router.delete(
    "/{hcp_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_hcp(
    hcp_id: int,
    db: Session = Depends(get_db),
) -> None:
    hcp = db.get(HCP, hcp_id)

    if hcp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="HCP not found.",
        )

    db.delete(hcp)
    db.commit()