from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.database.connection import get_session as get_db
from src.models.user import User
from src.schemas.user import (LoginRequest, LogoutResponse, Token, UserCreate,
                              UserResponse)
from src.services.auth_service import (authenticate_user, blacklist_token,
                                       create_access_token,
                                       get_current_active_user,
                                       get_current_token)
from src.services.auth_service import settings
from src.services.user_service import (create_user, get_user_by_email,
                                       get_user_by_username)

auth_router = APIRouter(
    prefix="/api/auth",
    tags=["Auth"]
)


@auth_router.post("/register", response_model=UserResponse,
                  status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=str(user.email))
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    return create_user(db=db, user=user)


@auth_router.post("/login", response_model=Token)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/logout", response_model=LogoutResponse)
async def logout(
        token: str = Depends(get_current_token),
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    """
    Logout endpoint that blacklists the current token.
    The token will be invalid for future requests.
    """
    try:
        # Decode token to get expiration time
        payload = jwt.decode(token, settings.secret_key,
                             algorithms=[settings.algorithm])
        exp = payload.get("exp")

        if exp:
            expires_at = datetime.fromtimestamp(exp)
        else:
            # If no expiration, set to default token lifetime from now
            expires_at = datetime.utcnow() + timedelta(
                minutes=settings.access_token_expire_minutes)

        # Add token to blacklist
        blacklist_token(db, token, expires_at)

        return LogoutResponse(
            message="Successfully logged out",
            detail=f"User {current_user.username} has been logged out"
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
