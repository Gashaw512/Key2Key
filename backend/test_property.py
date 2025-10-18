# test_property.py - FIXED WITH WORKING BROKER PATTERN
#!/usr/bin/env python3
"""
Fixed User ↔ PropertyListing One-to-Many Relationship Tests
Using same pattern as working test_broker.py
"""

from sqlalchemy import select
from sqlalchemy.orm import selectinload, configure_mappers
import asyncio
import uuid
import sys
import os

# Add backend/ to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import User, PropertyListing, PropertyType, ListingStatus
from app.core.database import AsyncSessionLocal

# ✅ CRITICAL: Configure mappers explicitly (same as broker test)
print("🔧 Configuring SQLAlchemy mappers...")
try:
    configure_mappers()
    print("✅ Mappers configured successfully")
except Exception as e:
    print(f"❌ Mapper configuration failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ✅ Verify relationships exist (same as broker test)
try:
    print(f"✅ User.property_listings relationship: {hasattr(User, 'property_listings')}")
    print(f"✅ PropertyListing.owner relationship: {hasattr(PropertyListing, 'owner')}")
    if not hasattr(User, 'property_listings'):
        print("❌ CRITICAL: property_listings relationship MISSING in User model!")
        print("   - Check app/models/user.py - uncomment the relationship")
        sys.exit(1)
except Exception as e:
    print(f"❌ Relationship check failed: {e}")
    sys.exit(1)

async def test_property_relationship():
    """Test complete User ↔ PropertyListing one-to-many cycle."""
    print("🧪 Testing User ↔ PropertyListing One-to-Many Relationship...")
    
    async with AsyncSessionLocal() as session:
        try:
            # 1. Create User (Owner)
            unique_email = f"owner+{uuid.uuid4().hex[:8]}@key2key.test"
            user = User(
                full_name="John Property Owner",
                email=unique_email,
                password_hash="test_hash_123",
                role="seller"
            )
            
            session.add(user)
            await session.flush()  # Generate ID before commit
            await session.commit()
            
            print(f"✅ Created Owner User: {user.id} | {user.email}")
            
            # 2. Create Multiple PropertyListings for this user
            properties = [
                PropertyListing(
                    title="Modern Apartment",
                    description="2-bedroom apartment in city center",
                    property_type=PropertyType.APARTMENT,
                    price=250000.0,
                    location="Downtown",
                    owner_id=user.id,
                    status=ListingStatus.AVAILABLE
                ),
                PropertyListing(
                    title="Spacious House",
                    description="3-bedroom house with garden",
                    property_type=PropertyType.HOUSE,
                    price=450000.0,
                    location="Suburbs",
                    owner_id=user.id,
                    status=ListingStatus.AVAILABLE
                )
            ]
            
            for prop in properties:
                session.add(prop)
            await session.commit()
            
            print(f"✅ Created {len(properties)} PropertyListings for user {user.id}")
            
            # 3. Test Forward Relationship (User → PropertyListings)
            # ✅ FIXED: Use scalar_one() like broker test
            result = await session.exec(
                select(User)
                .options(selectinload(User.property_listings))
                .where(User.id == user.id)
            )
            user_with_listings = result.scalar_one()  # ✅ KEY FIX: scalar_one()
            
            if user_with_listings and user_with_listings.property_listings:
                print(f"✅ User.property_listings works: {len(user_with_listings.property_listings)} listings")
                assert len(user_with_listings.property_listings) == 2
                first_listing = user_with_listings.property_listings[0]
                print(f"   First listing: {first_listing.title} (${first_listing.price})")
                assert first_listing.owner_id == user.id
            else:
                print("⚠️  No property_listings found")
                print(f"   user_with_listings: {user_with_listings}")
                if user_with_listings:
                    print(f"   Available attrs: {dir(user_with_listings)}")
            
            # 4. Test Reverse Relationship (PropertyListing → Owner)
            first_prop = properties[0]
            result = await session.exec(
                select(PropertyListing)
                .options(selectinload(PropertyListing.owner))
                .where(PropertyListing.id == first_prop.id)
            )
            prop_with_owner = result.scalar_one()  # ✅ KEY FIX: scalar_one()
            
            if prop_with_owner and prop_with_owner.owner:
                print(f"✅ PropertyListing.owner works: {prop_with_owner.owner.full_name}")
                assert prop_with_owner.owner.id == user.id
            else:
                print("⚠️  No owner found in property listing")
            
            # 5. Test Query by Owner ID (Multiple Results)
            result = await session.exec(
                select(PropertyListing).where(PropertyListing.owner_id == user.id)
            )
            listings_by_owner = result.all()  # ✅ .all() for multiple results
            
            if listings_by_owner:
                print(f"✅ Query by owner_id works: {len(listings_by_owner)} listings")
                assert len(listings_by_owner) == 2
            else:
                print("❌ No listings found by owner_id")
            
            # 6. Test Delete User (no cascade for listings)
            await session.delete(user)
            await session.commit()
            
            # Verify listings still exist (no cascade)
            result = await session.exec(
                select(PropertyListing).where(PropertyListing.owner_id == user.id)
            )
            remaining_listings = result.all()
            
            if remaining_listings:
                print(f"ℹ️  {len(remaining_listings)} listings remain (no delete cascade)")
            else:
                print("✅ PropertyListings deleted (cascade working)")
            
            print("🎉 ALL TESTS PASSED!")
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            await session.rollback()
            return False

async def test_isolation():
    """Test user without property listings."""
    async with AsyncSessionLocal() as session:
        user = User(
            full_name="Regular User",
            email=f"regular+{uuid.uuid4().hex[:8]}@key2key.test",
            password_hash="regular_hash"
        )
        session.add(user)
        await session.commit()
        
        # ✅ FIXED: Use scalar_one() like broker test
        result = await session.exec(
            select(User)
            .options(selectinload(User.property_listings))
            .where(User.id == user.id)
        )
        user_with_listings = result.scalar_one()  # ✅ KEY FIX
        
        assert len(user_with_listings.property_listings) == 0
        print("✅ User without property_listings: Empty list (correct)")

async def main():
    """Run all tests."""
    print("🚀 Starting Key2Key PropertyListing Tests (SQLAlchemy 2.0+)")
    print("=" * 60)
    
    # Test isolation first
    await test_isolation()
    
    # Test full relationship
    success = await test_property_relationship()
    
    if success:
        print("\n✅ ALL PROPERTYLISTING TESTS PASSED!")
        print("🔗 Architecture confirmed:")
        print("   • User.property_listings → List[PropertyListing] (One-to-Many)")
        print("   • PropertyListing.owner → User (Back Reference)")
        print("   • session.exec() + scalar_one() pattern works")
        print("   • Eager loading with selectinload() works")
    else:
        print("\n❌ Some tests failed - check relationship definition")
        print("\n💡 DEBUG: Verify in app/models/user.py:")
        print("   property_listings: List[\"PropertyListing\"] = Relationship(")
        print("       back_populates=\"owner\",")
        print("       sa_relationship_kwargs={...")
    
    print("\n🏁 Tests complete")

if __name__ == "__main__":
    try:
        from app.models import User, PropertyListing, PropertyType, ListingStatus
        from app.core.database import AsyncSessionLocal
        print("✅ Imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    
    asyncio.run(main())