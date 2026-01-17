from fastapi import APIRouter
from sqlalchemy.sql.functions import current_user

from schemas.user import UserResponse

user_router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)


@user_router.get("/me", response_model=UserResponse)
async def get_current_user():
    return UserResponse.from_orm(current_user)
