import enum
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class RoleEnum(str, enum.Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"
    RIDER = "RIDER"

class ParcelStatus(str, enum.Enum):
    PENDING = "PENDING"
    PICKED_UP = "PICKED_UP"
    IN_TRANSIT = "IN_TRANSIT"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.CUSTOMER)
    reset_token = Column(String, nullable=True)

    parcels = relationship("Parcel", back_populates="sender")

class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String, unique=True, index=True, nullable=False)
    sender_id = Column(Integer, ForeignKey("users.id"))
    recipient_name = Column(String, index=True, nullable=False)
    recipient_phone = Column(String, nullable=False)
    pickup_address = Column(String, nullable=False)
    delivery_address = Column(String, nullable=False)
    category = Column(String, index=True, nullable=False)
    weight_kg = Column(Float, default=1.0)
    delivery_charge = Column(Float, nullable=False)
    status = Column(Enum(ParcelStatus), default=ParcelStatus.PENDING, index=True)
    created_at = Column(DateTime, default=datetime.now, index=True)

    sender = relationship("User", back_populates="parcels")