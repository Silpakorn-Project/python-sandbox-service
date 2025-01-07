from fastapi import APIRouter
from app.schemas.user_schema import UserModel, NumberModel

router = APIRouter()

@router.post("/get")
async def getUser(user: UserModel):
    return {"users": ["user1", "user2"]}

@router.post("/addNumber")
async def getAddition(numbers: NumberModel):
    result = numbers.number1 + numbers.number2
    return {"result": result} 