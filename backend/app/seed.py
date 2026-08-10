from datetime import datetime, timedelta
from app.core.database import SessionLocal, engine, Base
from app.models.market import User, Listing, Bid  # Adjust imports to match your project setup

def create_user_instance(user_id: int, email: str, name_val: str):
    """Dynamically sets user fields including required password hashes."""
    user_kwargs = {}
    
    # Required primary key & constraint fields
    if hasattr(User, 'id'):
        user_kwargs['id'] = user_id
    if hasattr(User, 'email'):
        user_kwargs['email'] = email
    if hasattr(User, 'hashed_password'):
        # Mock bcrypt hash string to satisfy non-null database schema constraints
        user_kwargs['hashed_password'] = "$2b$12$eImiTXuWVxfM37uY4JANjOL.8/OHgA3vP9rTrAijfQ9u61iX4K66m"
    if hasattr(User, 'password'):
        user_kwargs['password'] = "mockpassword123"

    # Optional profile name fields
    if hasattr(User, 'username'):
        user_kwargs['username'] = name_val
    elif hasattr(User, 'name'):
        user_kwargs['name'] = name_val
    elif hasattr(User, 'full_name'):
        user_kwargs['full_name'] = name_val
        
    return User(**user_kwargs)

def seed_database():
    db = SessionLocal()
    
    # 1. Ensure tables exist in Postgres
    Base.metadata.create_all(bind=engine)
    
    # Avoid duplicate seeding
    if db.query(Listing).first():
        print("Database already contains seed data. Skipping...")
        db.close()
        return

    print("Seeding initial presentation data...")

    # 2. Add Test Users with required password fields
    user1 = create_user_instance(1, "seller@example.com", "TrackEnthusiast")
    user2 = create_user_instance(2, "buyer@example.com", "BimmerDriver")
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

    # 4. Add Initial Bid
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
    print("✅ Seeding complete! Sample listings and active bids loaded successfully.")

if __name__ == "__main__":
    seed_database()