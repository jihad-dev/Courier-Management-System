import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc

from database import get_db
from models import User, Parcel, ParcelStatus, RoleEnum
from router.auth import get_current_user

router = APIRouter(prefix="/user", tags=["User Parcel Management"])

class UserParcelCreate(BaseModel):
    recipient_name: str
    recipient_phone: str
    pickup_address: str
    delivery_address: str
    category: str
    weight_kg: float
    delivery_charge: float
@router.post("/parcels", status_code=status.HTTP_201_CREATED)
def create_user_parcel(
    parcel: UserParcelCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tracking_id = f"TRK-{uuid.uuid4().hex[:8].upper()}"
    new_parcel = Parcel(
        tracking_id=tracking_id,
        sender_id=current_user.id,
        **parcel.dict()
    )
    db.add(new_parcel)
    db.commit()
    db.refresh(new_parcel)
    return new_parcel


@router.get("/my-parcels")
def get_my_parcels(
    search: Optional[str] = Query(None, description="Search by tracking ID or recipient name"),
    status_filter: Optional[ParcelStatus] = Query(None),
    sort_by: str = Query("created_at", enum=["created_at", "delivery_charge"]),
    order: str = Query("desc", enum=["asc", "desc"]),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Parcel).filter(Parcel.sender_id == current_user.id)

    if search:
        query = query.filter(
            (Parcel.tracking_id.ilike(f"%{search}%")) |
            (Parcel.recipient_name.ilike(f"%{search}%"))
        )
    if status_filter:
        query = query.filter(Parcel.status == status_filter)

    sort_column = getattr(Parcel, sort_by)
    query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

    total = query.count()
    parcels = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": parcels
    }

@router.get("/track/{tracking_id}")
def track_parcel(tracking_id: str, db: Session = Depends(get_db)):
    parcel = db.query(Parcel).filter(Parcel.tracking_id == tracking_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found with this tracking ID")
    
    return {
        "tracking_id": parcel.tracking_id,
        "status": parcel.status,
        "pickup_address": parcel.pickup_address,
        "delivery_address": parcel.delivery_address,
        "created_at": parcel.created_at
    }
@router.put("/parcels/{parcel_id}/cancel")
def cancel_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    parcel = db.query(Parcel).filter(
        Parcel.id == parcel_id, 
        Parcel.sender_id == current_user.id
    ).first()

    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    if parcel.status != ParcelStatus.PENDING:
        raise HTTPException(status_code=400, detail="Cannot cancel parcel after it has been picked up or processed")

    parcel.status = ParcelStatus.CANCELLED
    db.commit()
    db.refresh(parcel)
    return {"message": "Parcel cancelled successfully", "parcel": parcel}