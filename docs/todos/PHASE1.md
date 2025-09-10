# Phase 1 — Configuration & Database

This phase ensures your app can read configuration safely and connect to the database with proper models and migrations.

---

## 1. Application Settings using Pydantic Settings

### Why?
Using **`pydantic-settings`** gives you type‑checked, validated configuration from environment variables or `.env` files.
This prevents misconfiguration and provides clear error messages when something is missing or malformed.

### Tasks:
- [x] Create `app/core/settings.py`.
- [x] Install `pydantic-settings` (either standalone or via `fastapi[all]`).
- [x] Define your `Settings` class:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    DATABASE_URL: str
    REDIS_URL: str
    JWT_SECRET: str
    ACCESS_TTL_MIN: int = 15
    REFRESH_TTL_DAYS: int = 30
    CORS_ORIGINS: List[str] = ["*"]
    ENV: str = "development"
    OPENROUTER_KEY: str = ""

settings = Settings()
```
- [ ] Add a FastAPI dependency for settings with `@lru_cache()`:
```python
from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    return Settings()
```

---

## 2. Create `.env.example`

Provide a clear template for required environment variables:

```dotenv
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/ruze
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your_jwt_secret_here
ACCESS_TTL_MIN=15
REFRESH_TTL_DAYS=30
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
ENV=development
OPENROUTER_KEY=your_key_here
```

---

## 3. Database Bootstrapping

### 3.1 Create Engine & Session
- [ ] `app/db/session.py`:
```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings

engine = create_async_engine(settings.DATABASE_URL, future=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
```
- [ ] `app/db/base.py`:
```python
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

### 3.2 Setup Alembic
- [ ] Run `alembic init alembic` (use `-t async` if needed).
- [ ] Configure `alembic/env.py` to reflect your models with `target_metadata = Base.metadata`.

---

## 4. Initial Data Models

- **`app/models/user.py`**:
```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

- **`app/models/refresh_token.py`**:
```python
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    jti = Column(String, unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, default=False)
    user = relationship("User", back_populates="refresh_tokens")

# In User model:
User.refresh_tokens = relationship("RefreshToken", back_populates="user")
```

---

## 5. Generate & Apply Migration
- [ ] Run:
```bash
alembic revision --autogenerate -m "initial schema"
alembic upgrade head
```
- [x] Verify table presence in DB (e.g. via `psql`, Adminer).

---

## 6. Definition of Done (DoD)
- [ ] App starts without errors.
- [ ] Settings load from `.env`.
- [ ] DB session is created successfully.
- [ ] `users` and `refresh_tokens` tables exist.
- (Optional) Add health check endpoint:
```python
@app.get("/health")
async def health_check(...):
    ...
```

---

## Quick Reference Table

| Task               | Description                                   |
|--------------------|-----------------------------------------------|
| Settings           | Typed config with defaults and `.env` support |
| `.env.example`     | Template for local setup                      |
| DB engine & session| Async SQLAlchemy setup                        |
| Data Models        | `User` and `RefreshToken` models              |
| Migrations         | Alembic setup and applied                     |
| DoD                | App starts fine, settings and tables validated|
