from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from settings import settings
# from authentication.auth import get_password_hash
# from user.models import DBUser, UserType


async def create_default_admin(session: AsyncSession):
    pass
    # result = await session.execute(select(DBUser).filter(DBUser.username == settings.ADMIN_USERNAME))
    # admin = result.unique().scalars().first()

    # if admin:
    #     print("Admin user already exists.")
    #     return

    # try:
    #     # If no admin exists, create one with secure credentials
    #     admin_user = DBUser(
    #         username=settings.ADMIN_USERNAME,
    #         email=settings.ADMIN_EMAIL,
    #         hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
    #         user_type=UserType.ADMIN,
    #         is_active=True
    #     )

    #     session.add(admin_user)
    #     await session.commit()
    #     await session.refresh(admin_user)
    #     print("Default admin user created successfully.")


    # except SQLAlchemyError as error:
    #     await session.rollback()
    #     raise HTTPException(status.HTTP_409_CONFLICT, f"{error}: Could not create user")
