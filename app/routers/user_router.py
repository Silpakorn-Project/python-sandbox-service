from fastapi import APIRouter, HTTPException
from app.services.user_service import SandboxService
from app.constant.error_constant import MISSING_FIELD

router = APIRouter()

@router.get("/testCode")
async def test_sandbox():
    "run code user on container and return output"
    total_score, total_cases = await SandboxService.grade_code()  
    return {"total_score": total_score, "total_cases": total_cases}

@router.get("/testCodeVm")
async def test_sandbox_container():
    "run code user on container and return output"
    try:
        user_code = """print(int(input())**3)"""
        test_input = """2"""

        if not user_code or not test_input:
            raise HTTPException(status_code=400, detail=MISSING_FIELD)

        output, error = await SandboxService.run_code_in_docker(user_code, test_input)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e