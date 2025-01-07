from fastapi import APIRouter
from app.schemas.user_schema import UserModel

router = APIRouter()

@router.post("/")
async def get_user(user: UserModel):
    return {"users": ["user1", "user2"]}

