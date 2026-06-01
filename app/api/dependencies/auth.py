# # app/api/dependencies/auth.py

# from fastapi import Depends
# from sqlalchemy.ext.asyncio import AsyncSession

# from app.api.db import get_db
# from app.crud.users import get_user


# async def get_current_user(
#     db: AsyncSession = Depends(get_db),
# ):
#     # later:
#     # read session cookie
#     # validate token
#     # lookup user

#     user = ...
#     return user