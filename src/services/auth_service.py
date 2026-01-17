from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from src.config.settings import settings
from src.database.connection import get_session as get_db
from src.models.user import User, TokenBlacklist
from src.schemas.user import TokenData

pwd_context = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    try:
        # Ensure password is a string and not too long
        if not isinstance(password, str):
            raise ValueError(f"Password must be a string, got {type(password)}")

        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            # Truncate to 72 bytes for bcrypt
            password_bytes = password_bytes[:72]
            password = password_bytes.decode('utf-8', errors='ignore')

        return pwd_context.hash(password)
    except Exception as e:
        # Add debugging info
        raise ValueError(f"Error hashing password (length: {len(password) 
            if isinstance(password, str) else 'N/A'}): {str(e)}")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key,
                             algorithm=settings.algorithm)
    return encoded_jwt

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def is_token_blacklisted(db: Session, token: str) -> bool:
    """Check if token is in blacklist"""
    blacklisted = db.query(TokenBlacklist).filter(
        TokenBlacklist.token == token
    ).first()
    return blacklisted is not None

def blacklist_token(db: Session, token: str, expires_at: datetime):
    """Add token to blacklist"""
    blacklisted_token = TokenBlacklist(
        token=token,
        expires_at=expires_at
    )
    db.add(blacklisted_token)
    db.commit()

def cleanup_expired_tokens(db: Session):
    """Remove expired tokens from blacklist (can be run periodically)"""
    db.query(TokenBlacklist).filter(
        TokenBlacklist.expires_at < datetime.utcnow()
    ).delete()
    db.commit()

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Check if token is blacklisted
    if is_token_blacklisted(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        username: str = payload.get("sub")
        exp: int = payload.get("exp")
        if username is None:
            raise credentials_exception
        token_data = TokenData(
            username=username,
            exp=datetime.fromtimestamp(exp) if exp else None
        )
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
        current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_token(token: str = Depends(oauth2_scheme)) -> str:
    """Dependency to extract the raw token"""
    return token
