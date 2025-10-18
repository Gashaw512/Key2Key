# app/services/user_service.py
"""
UserService — Business Logic for Key2Key Users
Handles CRUD, authentication, filtering, and stats.
"""

from typing import Optional, List
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy import func
from fastapi import HTTPException, status
from pydantic import UUID4, EmailStr
from sqlalchemy.exc import SQLAlchemyError

from app.models.user import User, UserCreate, UserRead, UserUpdate
from app.models.broker import BrokerProfile
from app.models.property import PropertyListing
from app.core.security import get_password_hash, verify_password
from app.core.logger import logger


class UserService:
    """Encapsulates all user-related operations."""

    # ----------------------------------------------------------------------
    # CREATE & AUTH
    # ----------------------------------------------------------------------
    async def create_user(self, db: AsyncSession, user_in: UserCreate) -> UserRead:
        try:
            existing = await self.get_user_by_email(db, user_in.email)
            if existing:
                raise HTTPException(400, detail="Email already registered.")

            user = User(
                **user_in.model_dump(exclude={"password"}),
                password_hash=get_password_hash(user_in.password)
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            logger.info(f"User created: {user.email}")
            return UserRead.model_validate(user)
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"DB error creating user {user_in.email}: {e}")
            raise HTTPException(500, "Database error")

    async def authenticate_user(self, db: AsyncSession, email: EmailStr, password: str) -> Optional[User]:
        user = await self.get_user_by_email(db, email)
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    # ----------------------------------------------------------------------
    # READ
    # ----------------------------------------------------------------------
    async def get_user_by_id(self, db: AsyncSession, user_id: UUID4, include_relations=False) -> Optional[UserRead]:
        try:
            query = select(User).where(User.id == user_id)
            if include_relations:
                from sqlalchemy.orm import selectinload
                query = query.options(
                    selectinload(User.broker_profile),
                    selectinload(User.property_listings),
                )
            result = await db.execute(query)
            user = result.scalar_one_or_none()
            return UserRead.model_validate(user) if user else None
        except SQLAlchemyError as e:
            logger.error(f"DB error fetching user {user_id}: {e}")
            raise HTTPException(500, "Database error")

    async def get_user_by_email(self, db: AsyncSession, email: EmailStr) -> Optional[User]:
        result = await db.exec(select(User).where(User.email == email))
        return result.one_or_none()

    # ----------------------------------------------------------------------
    # UPDATE & DELETE
    # ----------------------------------------------------------------------
    async def update_user(self, db: AsyncSession, user_id: UUID4, user_in: UserUpdate) -> Optional[UserRead]:
        try:
            db_user = await db.get(User, user_id)
            if not db_user:
                raise HTTPException(404, "User not found")

            updates = user_in.model_dump(exclude_unset=True)
            if "password" in updates:
                updates["password_hash"] = get_password_hash(updates.pop("password"))

            for key, value in updates.items():
                setattr(db_user, key, value)

            await db.commit()
            await db.refresh(db_user)
            return UserRead.model_validate(db_user)
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"DB error updating user {user_id}: {e}")
            raise HTTPException(500, "Database error")

    async def delete_user(self, db: AsyncSession, user_id: UUID4) -> bool:
        user = await db.get(User, user_id)
        if not user:
            return False
        await db.delete(user)
        await db.commit()
        return True

    # ----------------------------------------------------------------------
    # LISTING & SEARCH
    # ----------------------------------------------------------------------
    async def get_users_paginated(
        self, db: AsyncSession,
        skip: int = 0, limit: int = 100,
        role: Optional[str] = None,
        verified: Optional[bool] = None,
        email_contains: Optional[str] = None,
        sort_by: str = "created_at"
    ) -> List[UserRead]:
        try:
            query = select(User)
            if role:
                query = query.where(User.role == role)
            if verified is not None:
                query = query.where(User.verified == verified)
            if email_contains:
                query = query.where(User.email.ilike(f"%{email_contains}%"))

            if sort_by == "email":
                query = query.order_by(User.email.asc())
            else:
                query = query.order_by(User.created_at.desc())

            query = query.offset(skip).limit(limit)
            result = await db.exec(query)
            users = result.all()
            return [UserRead.model_validate(u) for u in users]
        except SQLAlchemyError as e:
            logger.error(f"DB error listing users: {e}")
            raise HTTPException(500, "Database error")

    async def search_users(self, db: AsyncSession, query: str, skip: int, limit: int) -> List[UserRead]:
        try:
            result = await db.exec(
                select(User).where(
                    (User.full_name.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
                ).offset(skip).limit(limit)
            )
            users = result.all()
            return [UserRead.model_validate(u) for u in users]
        except SQLAlchemyError as e:
            logger.error(f"DB error searching users: {e}")
            raise HTTPException(500, "Database error")

    # ----------------------------------------------------------------------
    # STATS
    # ----------------------------------------------------------------------
    async def get_user_stats(self, db: AsyncSession, user_id: UUID4) -> dict:
        try:
            listings = await db.exec(
                select(func.count()).select_from(PropertyListing).where(PropertyListing.owner_id == user_id)
            )
            broker = await db.get(BrokerProfile, user_id)
            return {
                "listings_count": listings.scalar() or 0,
                "is_broker": broker is not None
            }
        except SQLAlchemyError as e:
            logger.error(f"DB error getting user stats {user_id}: {e}")
            raise HTTPException(500, "Database error")
        

    # async def get_user_notifications_count(self, db: AsyncSession, user_id: UUID4) -> int:
    #     """Get count of notifications for a user."""
    #     try:
    #         result = await db.exec(
    #             select(func.count()).select_from(Notification)
    #             .where(Notification.user_id == user_id)
    #         )
    #         return result.scalar() or 0
    #     except SQLAlchemyError as e:
    #         logger.error(f"DB error counting notifications for user {user_id}: {e}")
    #         return 0

        

    

# Global instance
user_service = UserService()