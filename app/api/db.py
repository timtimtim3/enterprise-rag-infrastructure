# from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
# from dotenv import load_dotenv
# import os


# load_dotenv()
# DATABASE_URL = os.getenv("DATABASE_URL", "default")

# engine = create_async_engine(DATABASE_URL, echo=True)
# SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Base = declarative_base()


# async def get_db():
#     async with SessionLocal() as session:
#         yield session
