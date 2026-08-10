from pydantic import BaseModel, Field, model_validator
from datetime import datetime
from typing import Optional

# ==========================================
# LISTING / INVENTORY DATA CONTRACTS
# ==========================================

class ListingBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    condition: str = Field(..., description="e.g., 'Used - Like New', 'Fair - Track Wear'")
    starting_price: float = Field(..., gt=0)
    buy_now_price: Optional[float] = Field(None, gt=0)
    end_time: datetime

    @model_validator(mode="after")
    def validate_prices(self):
        """Cross-field validation to protect auction bounding logic"""
        if self.buy_now_price is not None and self.buy_now_price <= self.starting_price:
            raise ValueError("The 'Buy It Now' price must be higher than the starting price.")
        return self


class ListingCreate(ListingBase):
    """Schema used strictly during incoming POST listing requests"""
    owner_id: int  # Must link directly back to an existing User record


class ListingResponse(ListingBase):
    """Schema used for formatting outbound public API marketplace data"""
    id: int
    is_active: bool
    owner_id: int

    class Config:
        from_attributes = True


# ==========================================
# BIDDING DATA CONTRACTS
# ==========================================

class BidCreate(BaseModel):
    """Schema used when an external user submits an auction offer or buyout intent"""
    listing_id: int
    bidder_id: int  # Tracks who is trying to buy/bid on the item
    amount: float = Field(..., gt=0)


class BidResponse(BaseModel):
    """Schema used to structure confirmed auction feedback blocks"""
    id: int
    listing_id: int
    bidder_id: int
    amount: float
    is_buy_out: bool
    status: str
    timestamp: datetime

    class Config:
        from_attributes = True