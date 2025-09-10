from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.settings import settings
from sqlalchemy.orm import declarative_base

engine = create_async_engine(url=settings.DATABASE_URL, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()
