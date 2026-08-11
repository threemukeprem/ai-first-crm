from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.hcp import HCP
from app.schemas.hcp import HCPCreate, HCPUpdate


def create_hcp(db: Session, hcp_data: HCPCreate) -> HCP:
    hcp = HCP(**hcp_data.model_dump())

    db.add(hcp)
    db.commit()
    db.refresh(hcp)

    return hcp


def get_hcp_by_id(db: Session, hcp_id: int) -> HCP | None:
    return db.get(HCP, hcp_id)


def get_hcp_by_email(db: Session, email: str) -> HCP | None:
    statement = select(HCP).where(HCP.email == email)
    return db.scalar(statement)


def list_hcps(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[HCP]:
    statement = (
        select(HCP)
        .order_by(HCP.full_name.asc())
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def update_hcp(
    db: Session,
    hcp: HCP,
    hcp_data: HCPUpdate,
) -> HCP:
    update_data = hcp_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(hcp, field, value)

    db.add(hcp)
    db.commit()
    db.refresh(hcp)

    return hcp


def delete_hcp(db: Session, hcp: HCP) -> None:
    db.delete(hcp)
    db.commit()