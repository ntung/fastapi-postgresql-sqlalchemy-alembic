from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.models.base import Base


class User(Base):
    """
    A class to represent a user
    """
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TokenBlacklist(Base):
    """
    A class to represent a blacklisted user
    """
    __tablename__ = "token_blacklist"
    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    blacklisted_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
