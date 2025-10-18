# # Generic relationship test template
# async def test_relationship(parent_model, child_model, parent_rel_name, child_rel_name):
#     """Generic bidirectional relationship test."""
    
#     # 1. Create parent
#     parent = parent_model(...)
#     session.add(parent)
#     await session.commit()
    
#     # 2. Create children
#     children = [child_model(parent_id=parent.id, ...) for _ in range(2)]
#     for child in children:
#         session.add(child)
#     await session.commit()
    
#     # 3. Test forward (parent → children)
#     result = await session.exec(
#         select(parent_model)
#         .options(selectinload(getattr(parent_model, parent_rel_name)))
#         .where(parent_model.id == parent.id)
#     )
#     parent_with_rel = result.scalar_one()
#     assert len(getattr(parent_with_rel, parent_rel_name)) == 2
    
#     # 4. Test reverse (child → parent)
#     child = children[0]
#     result = await session.exec(
#         select(child_model)
#         .options(selectinload(getattr(child_model, child_rel_name)))
#         .where(child_model.id == child.id)
#     )
#     child_with_rel = result.scalar_one()
#     assert child_with_rel.parent_rel_name.id == parent.id