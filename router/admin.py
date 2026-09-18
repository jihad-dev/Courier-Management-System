import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from database import get_db
from models import User, Parcel, RoleEnum, ParcelStatus
from router.auth import get_current_user

router = APIRouter(prefix="/admin", tags=["Admin & Logistics Management"])

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

class ParcelCreate(BaseModel):
    recipient_name: str
    recipient_phone: str
    pickup_address: str
    delivery_address: str
    category: str
    weight_kg: float
    delivery_charge: float

class ParcelUpdate(BaseModel):
    status: Optional[ParcelStatus] = None
    delivery_address: Optional[str] = None

# ONLY ADMIN CAN ACCESS THIS ROUTE
@router.get("/parcels")
def list_parcels(
    search: Optional[str] = Query(None, description="Search by tracking ID or recipient name"),
    category: Optional[str] = Query(None),
    status_filter: Optional[ParcelStatus] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    sort_by: str = Query("created_at", enum=["created_at", "delivery_charge", "recipient_name"]),
    order: str = Query("desc", enum=["asc", "desc"]),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    query = db.query(Parcel)

    if search:
        query = query.filter(
            (Parcel.tracking_id.ilike(f"%{search}%")) |
            (Parcel.recipient_name.ilike(f"%{search}%"))
        )
    if category:
        query = query.filter(Parcel.category == category)
    if status_filter:
        query = query.filter(Parcel.status == status_filter)
    if start_date and end_date:
        query = query.filter(Parcel.created_at.between(start_date, end_date))

    sort_column = getattr(Parcel, sort_by)
    query = query.order_by(desc(sort_column) if order == "desc" else asc(sort_column))

    total = query.count()
    parcels = query.offset((page - 1) * page_size).limit(page_size).all()

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
        "data": parcels
    }

# 2. CRUD Operations
@router.post("/parcels", status_code=status.HTTP_201_CREATED)
def create_parcel(
    parcel: ParcelCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    tracking_id = f"TRK-{uuid.uuid4().hex[:8].upper()}"
    new_parcel = Parcel(
        tracking_id=tracking_id,
        sender_id=admin.id,
        **parcel.dict()
    )
    db.add(new_parcel)
    db.commit()
    db.refresh(new_parcel)
    return new_parcel

@router.get("/parcels/{parcel_id}")
def get_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")
    return parcel

@router.put("/parcels/{parcel_id}")
def update_parcel(
    parcel_id: int,
    data: ParcelUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(parcel, key, value)

    db.commit()
    db.refresh(parcel)
    return parcel

@router.delete("/parcels/{parcel_id}")
def delete_parcel(
    parcel_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin)
):
    parcel = db.query(Parcel).filter(Parcel.id == parcel_id).first()
    if not parcel:
        raise HTTPException(status_code=404, detail="Parcel not found")

    db.delete(parcel)
    db.commit()
    return {"message": f"Parcel {parcel_id} deleted successfully"}