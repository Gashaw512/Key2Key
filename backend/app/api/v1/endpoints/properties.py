# app/api/v1/endpoints/properties.py
# @app.post("/properties/", response_model=PropertyListingRead)
# async def create_property(
#     property_in: PropertyListingCreate,
#     current_user: User = Depends(get_current_user)
# ):
#     # Set owner_id from authenticated user
#     db_property = PropertyListing(**property_in.dict(), owner_id=current_user.id)
#     session.add(db_property)
#     await session.commit()
#     await session.refresh(db_property)
#     return db_property

# @app.get("/users/{user_id}/properties", response_model=List[PropertyListingRead])
# async def get_user_properties(user_id: uuid.UUID):
#     result = await session.exec(
#         select(PropertyListing)
#         .options(selectinload(PropertyListing.owner))
#         .where(PropertyListing.owner_id == user_id)
#     )
#     return result.all()