# app/services/broker_service.py
"""
Production-Ready BrokerProfile Service
Handles CRUD with user linking, validation, and error handling.
"""

from typing import Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import and_, func
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import joinedload


from app.models.broker import (
    BrokerProfile, BrokerProfileCreate, BrokerProfileRead, BrokerProfileUpdate
)
from app.models.user import User
from app.core.logger import logger

class BrokerService:
    """Manages BrokerProfile business logic with user relationships."""
    
    async def create_broker_profile(
        self, 
        db: AsyncSession, 
        broker_create: BrokerProfileCreate,
        user_id: UUID4
    ) -> BrokerProfileRead:
        """Create broker profile linked to existing user."""
        try:
            # 1. Verify user exists
            user = await db.get(User, user_id)
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            # 2. Check if user already has broker profile
            existing = await self.get_by_user_id(db, user_id)
            if existing:
                raise HTTPException(
                    status_code=409,
                    detail="User already has a broker profile"
                )
            
            # 3. Create broker profile
            broker_data = broker_create.model_dump()
            db_broker = BrokerProfile(
                **broker_data,
                user_id=user_id
            )
            
            # 4. Save and link
            db.add(db_broker)
            await db.flush()  # Generate ID
            await db.commit()
            await db.refresh(db_broker)
            
            # 5. Refresh user to load relationship
            await db.refresh(user)
            
            logger.info(f"Broker profile created: {db_broker.id} for user {user_id}")
            return BrokerProfileRead.model_validate(db_broker)
            
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"DB error creating broker profile: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    
    async def get_broker_by_id(self, db: AsyncSession, broker_id: UUID4) -> Optional[BrokerProfileRead]:
        """Get broker profile by ID with user relationship."""
        try:
            result = await db.exec(
                select(BrokerProfile)
                .options(joinedload(BrokerProfile.user))
                .where(BrokerProfile.id == broker_id)
            )
            broker = result.one_or_none()
            if not broker:
                return None
            return BrokerProfileRead.model_validate(broker)
        except SQLAlchemyError as e:
            logger.error(f"DB error getting broker {broker_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    
    async def get_by_user_id(self, db: AsyncSession, user_id: UUID4) -> Optional[BrokerProfileRead]:
        """Get broker profile by user ID (one-to-one)."""
        try:
            result = await db.exec(
                select(BrokerProfile)
                .options(joinedload(BrokerProfile.user))
                .where(BrokerProfile.user_id == user_id)
            )
            broker = result.one_or_none()
            if not broker:
                return None
            return BrokerProfileRead.model_validate(broker)
        except SQLAlchemyError as e:
            logger.error(f"DB error getting broker for user {user_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    
    async def update_broker_profile(
        self, 
        db: AsyncSession, 
        broker_id: UUID4, 
        broker_update: BrokerProfileUpdate
    ) -> Optional[BrokerProfileRead]:
        """Partial update broker profile."""
        try:
            db_broker = await db.get(BrokerProfile, broker_id)
            if not db_broker:
                raise HTTPException(status_code=404, detail="Broker profile not found")
            
            # Apply partial updates
            update_data = broker_update.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_broker, key, value)
            
            await db.commit()
            await db.refresh(db_broker)
            
            logger.info(f"Broker profile updated: {broker_id}")
            return BrokerProfileRead.model_validate(db_broker)
            
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"DB error updating broker {broker_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    
    async def delete_broker_profile(self, db: AsyncSession, broker_id: UUID4) -> bool:
        """Delete broker profile (user remains)."""
        try:
            db_broker = await db.get(BrokerProfile, broker_id)
            if not db_broker:
                raise HTTPException(status_code=404, detail="Broker profile not found")
            
            await db.delete(db_broker)
            await db.commit()
            
            logger.warning(f"Broker profile deleted: {broker_id}")
            return True
            
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"DB error deleting broker {broker_id}: {e}")
            raise HTTPException(status_code=500, detail="Database error")
    
    async def list_broker_profiles(
        self, 
        db: AsyncSession, 
        skip: int = 0, 
        limit: int = 100,
        is_verified: Optional[bool] = None
    ) -> List[BrokerProfileRead]:
        """Paginated list with filtering, handles NULL user_id."""
        try:
            query = select(BrokerProfile).offset(skip).limit(limit)
            
            # Filter out invalid records with NULL user_id
            query = query.where(BrokerProfile.user_id != None)
            
            if is_verified is not None:
                query = query.where(BrokerProfile.is_verified == is_verified)
            
            query = query.order_by(BrokerProfile.created_at.desc())
            
            result = await db.exec(query)
            brokers = result.all()
            
            # Log any problematic records
            validated_brokers = []
            for broker in brokers:
                try:
                    validated_brokers.append(BrokerProfileRead.model_validate(broker))
                except Exception as e:
                    logger.warning(f"Skipping invalid broker profile {broker.id}: {e}")
            
            logger.info(f"Listed {len(validated_brokers)} valid broker profiles")
            return validated_brokers
        except SQLAlchemyError as e:
            logger.error(f"DB error listing brokers: {e}")
            raise HTTPException(status_code=500, detail="Failed to list brokers")
    
    async def get_broker_count(self, db: AsyncSession, is_verified: Optional[bool] = None) -> int:
        """Get total broker count."""
        try:
            query = select(func.count()).select_from(BrokerProfile)
            if is_verified is not None:
                query = query.where(BrokerProfile.is_verified == is_verified)
            
            result = await db.exec(query)
            return result.scalar() or 0
            
        except SQLAlchemyError as e:
            logger.error(f"DB error counting brokers: {e}")
            raise HTTPException(status_code=500, detail="Failed to count brokers")

# Global instance
broker_service = BrokerService()