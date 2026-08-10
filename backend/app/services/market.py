from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.market import Listing, Bid
from app.api.schemas.market import ListingCreate, BidCreate

class MarketService:
    @staticmethod
    def create_listing(db: Session, listing_data: ListingCreate) -> Listing:
        """Takes validated schema data and saves a new active listing to PostgreSQL"""
        db_listing = Listing(**listing_data.model_dump())
        db.add(db_listing)
        db.commit()
        db.refresh(db_listing)
        return db_listing

    @staticmethod
    def get_active_listings(db: Session, skip: int = 0, limit: int = 100):
        """Fetches active, unsold market items for users to browse"""
        return db.query(Listing).filter(Listing.is_active == True).offset(skip).limit(limit).all()

    @staticmethod
    def handle_bid_or_buyout(db: Session, bid_data: BidCreate) -> Bid:
        """Processes offer inputs: triggers an instant buyout or standard bid constraints"""
        # 1. Verify listing is active and available
        listing = db.query(Listing).filter(Listing.id == bid_data.listing_id, Listing.is_active == True).first()
        if not listing:
            raise HTTPException(status_code=404, detail="This marketplace listing is no longer active.")
        
        # 2. Prevent a user from bidding on their own item
        if listing.owner_id == bid_data.bidder_id:
            raise HTTPException(status_code=400, detail="Sellers cannot submit offers on their own listings.")

        # 3. CRITICAL ENGINE PATHWAY: INSTANT BUYOUT RULE
        if listing.buy_now_price and bid_data.amount >= listing.buy_now_price:
            # Commit the direct buyout event transaction record
            db_buyout = Bid(
                listing_id=bid_data.listing_id,
                bidder_id=bid_data.bidder_id,
                amount=listing.buy_now_price,  # Locks transaction at exact buyout valuation
                is_buy_out=True,
                status="accepted_buyout"
            )
            # Deactivate listing instantly so it drops off active search pages
            listing.is_active = False
            
            # Instantly update all legacy un-resolved bids to an 'outbid' state
            db.query(Bid).filter(Bid.listing_id == listing.id, Bid.status == "pending").update({"status": "outbid"})
            
            db.add(db_buyout)
            db.commit()
            db.refresh(db_buyout)
            return db_buyout

        # 4. TRADITIONAL AUCTION RULES ENGINE
        if bid_data.amount < listing.starting_price:
            raise HTTPException(
                status_code=400, 
                detail=f"Bid amount must meet the minimum entry requirement of ${listing.starting_price}"
            )
        
        # Identify the previous leading competitor offer
        highest_bid = db.query(Bid).filter(Bid.listing_id == bid_data.listing_id).order_by(Bid.amount.desc()).first()
        if highest_bid and bid_data.amount <= highest_bid.amount:
            raise HTTPException(
                status_code=400, 
                detail=f"Bid too low. The current leading offer is ${highest_bid.amount}"
            )

        # 5. COMMIT COMPLETED OPEN-MARKET BID
        db_bid = Bid(**bid_data.model_dump(), is_buy_out=False, status="pending")
        if highest_bid:
            highest_bid.status = "outbid"  # Mark old top bid out of the race
            
        db.add(db_bid)
        db.commit()
        db.refresh(db_bid)
        return db_bid