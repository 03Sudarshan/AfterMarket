import datetimefrom 
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Core relationship channels
    listings = relationship("Listing", back_populates="owner", cascade="all, delete-orphan")
    bids = relationship("Bid", back_populates="bidder", cascade="all, delete-orphan")

class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True, index=False)
    title= Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    reserve_price = Column(Float, nullable=False)
    current_highest_bid = Column(Float, default=0.0)
    is_active = Column(Boolean, default=True)
    end_time = Column(DateTime, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User", back_populates="listings")
    bids = relationship("Bid", back_populates="listing", cascade="all, delete-orphan")

class Bid(Base):
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    listing_id = Column(Integer, ForeignKey("listings.id", ondelete="CASCADE"), nullable=False)
    bidder_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    listing = relationship("Listing", back_populates="bids")
    bidder = relationship("User", back_populates="bids")