from app.core.database import SessionLocal, engine, Base
from app.models.market import User, Listing, Bid  # Adjust model imports to match your file structure
from datetime import datetime, timedelta

def seed_database():
    db = SessionLocal()
    
    # 1. Ensure tables exist
    Base.metadata.create_all(bind=engine)
    
    # Check if data already exists to avoid duplication
    if db.query(Listing).first():
        print("Database already contains seed data. Skipping...")
        db.close()
        return

    print("Seeding initial presentation data...")

    # 2. Add Test Users
    user1 = User(id=1, username="TrackEnthusiast", email="seller@example.com")
    user2 = User(id=2, username="BimmerDriver", email="buyer@example.com")
    db.add_all([user1, user2])
    db.commit()

    # 3. Add Sample Listings
    listing1 = Listing(
        id=1,
        title="825M Style Replica Rims - Set of 4",
        description="Clean track-build style offset. Light curb rash on rear right, perfect for track setup.",
        condition="Used - Good",
        starting_price=600.0,
        buy_now_price=1200.0,
        is_active=True,
        end_time=datetime.utcnow() + timedelta(days=7),
        owner_id=1
    )
    
    listing2 = Listing(
        id=2,
        title="Custom Shadowline Aftermarket Headlights",
        description="Custom painted housing with updated LED rings. Plug and play harness included.",
        condition="Like New",
        starting_price=450.0,
        buy_now_price=850.0,
        is_active=True,
        end_time=datetime.utcnow() + timedelta(days=3),
        owner_id=1
    )

    db.add_all([listing1, listing2])
    db.commit()

    # 4. Add Initial Bids
    bid1 = Bid(
        listing_id=1,
        bidder_id=2,
        amount=650.0,
        is_buy_out=False,
        status="active",
        timestamp=datetime.utcnow()
    )
    
    db.add(bid1)
    db.commit()
    db.close()
    print("Seeding complete! Sample listings and active bids loaded.")

if __name__ == "__main__":
    seed_database()