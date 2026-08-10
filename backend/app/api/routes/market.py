from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.market import MarketService
from app.api.schemas.market import (
    ListingCreate, ListingResponse,
    BidCreate, BidResponse
)

router = APIRouter(prefix="/market", tags=["Market Engine"])

@router.post("/items", response_model=ListingResponse, status_code=status.HTTP_201_CREATED)
def create_new_listing(item: ListingCreate, db: Session = Depends(get_db)):
    """Exposes a secure POST path to launch a brand new aftermarket listing."""
    return MarketService.create_listing(db, item)

@router.get("/items", response_model=List[ListingResponse])
def list_all_active_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Exposes a clean GET feed returning only active marketplace listings."""
    return MarketService.get_active_listings(db, skip, limit)

@router.post("/bids", response_model=BidResponse, status_code=status.HTTP_201_CREATED)
def submit_bid_or_buyout_intent(bid: BidCreate, db: Session = Depends(get_db)):
    """Exposes a transactional POST route to process incoming bids or buyout claims."""
    return MarketService.handle_bid_or_buyout(db, bid)