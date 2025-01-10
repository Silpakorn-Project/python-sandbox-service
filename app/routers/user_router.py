from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserModel, NumberModel
from app.services.user_service import UserService


router = APIRouter()

@router.post("/get")
async def getUser(user: UserModel):
    return {"users": ["user1", "user2"]}

@router.post("/addNumber")
async def getAddition(numbers: NumberModel):
    result = numbers.number1 + numbers.number2
    return {"result": result} 

@router.get("/getTest")
async def testCode():
    return UserService.getUsers()

# No vm
@router.get("/testCode")
async def testCode():
    total_score, total_cases = await UserService.grade_code()  
    return {"total_score": total_score, "total_cases": total_cases}


@router.get("/testCodeVm")
async def test_code_vm():
    try:
        user_code = """
print(int(input())**3)
"""
        test_input = """2""" 

        if not user_code or not test_input:
            raise HTTPException(status_code=400, detail="Missing 'code' or 'input' field")

        output, error = await UserService.run_code_in_docker(user_code, test_input)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



