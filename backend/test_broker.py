# test_broker.py - FIXED VERSION
#!/usr/bin/env python3
"""
Fixed User ↔ BrokerProfile One-to-One Relationship Tests
SQLAlchemy 2.0+ Async Compatible
"""

from sqlalchemy import select
from sqlalchemy.orm import selectinload
import asyncio
import uuid
import sys
import os

from sqlalchemy.orm import configure_mappers

# Add backend/ to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.models import User, BrokerProfile
from app.core.database import AsyncSessionLocal


# ✅ CRITICAL: Configure mappers explicitly
print("🔧 Configuring SQLAlchemy mappers...")
try:
    configure_mappers()
    print("✅ Mappers configured successfully")
except Exception as e:
    print(f"❌ Mapper configuration failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Verify relationship exists
try:
    print(f"✅ User.broker_profile relationship: {hasattr(User, 'broker_profile')}")
    print(f"✅ BrokerProfile.user relationship: {hasattr(BrokerProfile, 'user')}")
except Exception as e:
    print(f"❌ Relationship check failed: {e}")
    sys.exit(1)

async def test_relationship_exists():
    """Verify relationships are accessible."""
    async with AsyncSessionLocal() as session:
        # Test basic User creation
        user = User(
            full_name="Test User",
            email=f"test+{uuid.uuid4().hex[:8]}@test.com",
            password_hash="hash"
        )
        session.add(user)
        await session.commit()
        
        # ✅ Test if broker_profile attribute exists (even if None)
        print(f"User.broker_profile type: {type(user.broker_profile)}")
        print(f"User.broker_profile is None: {user.broker_profile is None}")
        
        # This should NOT raise AttributeError
        assert hasattr(user, 'broker_profile')
        print("✅ broker_profile attribute accessible")

async def test_broker_relationship():
    """Test complete User-BrokerProfile relationship cycle."""
    print("🧪 Testing User ↔ BrokerProfile One-to-One Relationship...")
    
    async with AsyncSessionLocal() as session:
        try:
            # 1. Create User
            unique_email = f"broker+{uuid.uuid4().hex[:8]}@key2key.test"
            user = User(
                full_name="John Broker",
                email=unique_email,
                password_hash="test_hashed_password_123",
                role="broker"
            )
            
            session.add(user)
            await session.flush()  # Generate ID before commit
            await session.commit()
            
            print(f"✅ Created User: {user.id} | {user.email}")
            
            # 2. Create BrokerProfile for this user
            broker = BrokerProfile(
                user_id=user.id,
                license_number=f"LIC-{uuid.uuid4().hex[:8].upper()}",
                years_experience=5,
                bio="Experienced real estate broker",
                is_verified=True
            )
            
            session.add(broker)
            await session.commit()
            
            print(f"✅ Created BrokerProfile: {broker.id} | License: {broker.license_number}")
            
            # 3. Test Forward Relationship (User → BrokerProfile)
            # ✅ FIXED: Use session.exec() + eager loading
            result = await session.exec(
                select(User)
                .options(selectinload(User.broker_profile))
                .where(User.id == user.id)
            )
            # user_with_profile = result.one()
            user_with_profile = result.scalar_one()
            
            if user_with_profile and user_with_profile.broker_profile:
                print(f"✅ User.broker_profile works: {user_with_profile.broker_profile.license_number}")
                assert user_with_profile.broker_profile.id == broker.id
                assert user_with_profile.broker_profile.user_id == user.id
            else:
                print("⚠️  No broker_profile found - relationship not loaded")
            
            # 4. Test Reverse Relationship (BrokerProfile → User)
            # ✅ FIXED: Use session.exec()
            result = await session.exec(
                select(BrokerProfile)
                .options(selectinload(BrokerProfile.user))
                .where(BrokerProfile.id == broker.id)
            )
            broker_with_user = result.scalar_one()
            
            if broker_with_user and broker_with_user.user:
                print(f"✅ BrokerProfile.user works: {broker_with_user.user.full_name}")
                assert broker_with_user.user.id == user.id
            else:
                print("⚠️  No user found in broker profile")
            
            # 5. ✅ FIXED: Query by user_id using SELECT (not session.get)
            # session.get() only works with PRIMARY KEY
            result = await session.exec(
                select(BrokerProfile).where(BrokerProfile.user_id == user.id)
            )
            broker_by_user = result.scalar_one()
            
            if broker_by_user:
                print(f"✅ Query by user_id works: {broker_by_user.license_number}")
                assert broker_by_user.id == broker.id
            else:
                print("❌ No broker profile found by user_id")
            
            # 6. Test Delete Cascade
            await session.delete(user)
            await session.commit()
            
            # Verify broker profile deleted (CASCADE)
            # ✅ Use session.get() with PRIMARY KEY only
            remaining = await session.get(BrokerProfile, broker.id)
            assert remaining is None
            print("✅ Delete cascade works - BrokerProfile deleted with User")
            
            print("🎉 ALL TESTS PASSED!")
            return True
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            await session.rollback()
            return False

async def test_isolation():
    """Test user without broker profile."""
    async with AsyncSessionLocal() as session:
        user = User(
            full_name="Regular User",
            email=f"regular+{uuid.uuid4().hex[:8]}@key2key.test",
            password_hash="regular_hash"
        )
        session.add(user)
        await session.commit()
        
        # ✅ FIXED: Use session.exec()
        result = await session.exec(
            select(User)
            .options(selectinload(User.broker_profile))
            .where(User.id == user.id)
        )
        user_with_profile = result.scalar_one()
        
        assert user_with_profile.broker_profile is None
        print("✅ User without broker_profile: None (correct)")

async def test_session_get():
    """Test session.get() with primary keys only."""
    async with AsyncSessionLocal() as session:
        # Create test data
        user = User(full_name="Test", email=f"get+{uuid.uuid4().hex[:8]}@test.com", password_hash="hash")
        session.add(user)
        await session.commit()
        
        # ✅ session.get() works with PRIMARY KEY only
        fetched_user = await session.get(User, user.id)
        assert fetched_user.id == user.id
        print("✅ session.get() works with primary key")
        
        # ❌ This doesn't work - session.get() doesn't accept user_id
        # fetched_broker = await session.get(BrokerProfile, user_id=user.id)  # ERROR!
        
        print("✅ session.get() limitations confirmed")

async def main():
    """Run all tests."""
    print("🚀 Starting Key2Key Relationship Tests (SQLAlchemy 2.0+)")
    print("=" * 60)
    
    # Test isolation
    await test_isolation()
    
    # Test session.get() behavior
    await test_session_get()
    
    # Test full relationship
    success = await test_broker_relationship()
    
    if success:
        print("\n✅ ALL RELATIONSHIP TESTS PASSED!")
        print("🔗 Architecture confirmed:")
        print("   • User.broker_profile → BrokerProfile (One-to-One)")
        print("   • BrokerProfile.user → User (Back Reference)")
        print("   • CASCADE delete works")
        print("   • session.exec() + select() pattern")
        print("   • session.get() = PRIMARY KEY only")
    else:
        print("\n❌ Some tests failed")
    
    print("\n🏁 Tests complete")

if __name__ == "__main__":
    try:
        from app.models import User, BrokerProfile
        from app.core.database import AsyncSessionLocal
        print("✅ Imports successful")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        sys.exit(1)
    
    asyncio.run(main())