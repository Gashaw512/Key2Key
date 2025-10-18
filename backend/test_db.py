# test_db_fixed.py - Handles datetime and UUID properly
#!/usr/bin/env python3
"""
Fixed Key2Key Test Script - Proper Type Handling for datetime & UUID
"""

import asyncio
import sys
import uuid
from datetime import datetime, timezone
from typing import get_origin, get_args
from contextlib import asynccontextmanager

from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

# Project imports
try:
    from app.core.database import async_engine, AsyncSessionLocal
    from app.core.logger import logger
    from app.models.user import User
    print("✅ Project imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

@asynccontextmanager
async def get_test_session():
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

def create_proper_test_data(required_fields):
    """Create test data with correct types for datetime and UUID."""
    test_data = {
        "full_name": "Database Test User",
        "email": f"dbtest+{uuid.uuid4().hex[:8]}@example.com",
        "password_hash": "db_test_hash",
        "phone": None,
        "role": "buyer",  # Enum will handle conversion
        "verified": False,
    }
    
    # Handle special types for required fields
    for field in required_fields:
        if field == "created_at":
            # ✅ Proper datetime
            test_data[field] = datetime.now(timezone.utc)
        elif field == "id":
            # ✅ Proper UUID or let database generate
            test_data[field] = None  # Let DB generate UUID
        elif field not in test_data:
            test_data[field] = "default_value"
    
    # Remove id if database auto-generates it
    if "id" in test_data and test_data["id"] is None:
        del test_data["id"]
    
    return test_data

async def test_database_creation():
    """Test database operations with proper type handling."""
    print("🗄️ Testing database operations with proper types...")
    
    # Get model fields to identify required ones
    model_fields = getattr(User, 'model_fields', getattr(User, '__fields__', {}))
    required_fields = []
    
    for field_name, field_info in model_fields.items():
        # Skip if has default or is optional
        if hasattr(field_info, 'default') and field_info.default != ...:
            continue
        required_fields.append(field_name)
    
    print(f"Required fields detected: {required_fields}")
    
    # Create properly typed test data
    test_data = create_proper_test_data(required_fields)
    print(f"Test data with proper types: {test_data}")
    
    async with get_test_session() as session:
        try:
            print(f"Creating user: {test_data.get('email', 'N/A')}")
            
            # Create user instance
            db_user = User(**test_data)
            print(f"User instance created with ID: {getattr(db_user, 'id', 'Will be generated')}")
            
            # Add to session
            session.add(db_user)
            await session.flush()  # Flush to generate ID if auto-generated
            
            print(f"After flush - ID: {db_user.id}")
            await session.commit()
            await session.refresh(db_user)
            
            print(f"✅ DATABASE CREATION SUCCESS!")
            print(f"   ID: {db_user.id}")
            print(f"   Email: {db_user.email}")
            print(f"   Created at: {db_user.created_at}")
            
            # Verify with query
            result = await session.exec(select(User).where(User.id == db_user.id))
            verified = result.one_or_none()
            
            if verified:
                print(f"✅ VERIFICATION SUCCESS: {verified.email}")
                
                # Test API-style query
                result = await session.exec(select(User).limit(5))
                users = result.all()
                print(f"✅ API QUERY TEST: Found {len(users)} users")
                
                # Show user details
                print("Created user details:")
                for attr in ['id', 'full_name', 'email', 'role', 'created_at']:
                    if hasattr(verified, attr):
                        value = getattr(verified, attr)
                        print(f"  {attr}: {value}")
                
                return True
            else:
                print("❌ Verification failed")
                return False
                
        except IntegrityError as e:
            await session.rollback()
            print(f"❌ INTEGRITY ERROR: {e}")
            print("💡 Check unique constraints (email must be unique)")
            return False
        except Exception as e:
            await session.rollback()
            print(f"❌ DATABASE ERROR: {type(e).__name__}: {e}")
            print("Test data used:", test_data)
            import traceback
            traceback.print_exc()
            return False

async def test_api_ready():
    """Test the exact API query that your endpoint uses."""
    print("\n🔍 Testing API-ready query...")
    
    async with get_test_session() as session:
        try:
            # This is what your FastAPI endpoint likely does
            result = await session.exec(select(User))
            users = result.all()
            
            print(f"✅ API endpoint simulation: Found {len(users)} users")
            
            if users:
                sample_user = users[0]
                print(f"Sample user:")
                print(f"  ID: {sample_user.id}")
                print(f"  Name: {sample_user.full_name}")
                print(f"  Email: {sample_user.email}")
                
                # Test Pydantic serialization
                user_dict = sample_user.dict() if hasattr(sample_user, 'dict') else vars(sample_user)
                print(f"  JSON serializable: {len(user_dict)} fields")
                
            return len(users) > 0
            
        except Exception as e:
            print(f"❌ API simulation failed: {e}")
            return False

async def main():
    """Main test function."""
    print("=" * 70)
    print("🔧 Key2Key FIXED Database Test (Proper Type Handling)")
    print("=" * 70)
    
    try:
        # Test 1: Database creation
        db_ok = await test_database_creation()
        
        if db_ok:
            # Test 2: API simulation
            api_ok = await test_api_ready()
            
            if api_ok:
                print("\n" + "=" * 70)
                print("🎉 COMPLETE SUCCESS!")
                print("✅ Database operations: PASSED")
                print("✅ API simulation: PASSED")
                print("✅ Proper datetime & UUID handling")
                print("\n💡 Your API endpoint is now ready!")
                print("💡 Test it with:")
                print("   curl http://127.0.0.1:8000/api/v1/users/")
                print("\n✅ Expected response:")
                print('[{"id": "uuid", "full_name": "Database Test User", "email": "dbtest+...", ...}]')
            else:
                print("\n⚠️  API simulation failed")
        else:
            print("\n💥 Database creation failed")
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🏁 Test completed")

if __name__ == "__main__":
    import pydantic
    print(f"Pydantic version: {pydantic.VERSION}")
    asyncio.run(main())