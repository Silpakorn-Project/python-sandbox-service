"Module FastApi"
from fastapi import APIRouter, HTTPException
from app.schemas.request_schema import SandboxRequest
from app.schemas.response_schema import SubmitResponseAll
from app.services.sandbox_service import SandboxService
from app.constant.error_constant import MISSING_FIELD

router = APIRouter()

@router.get("/test-code")
async def test_sandbox() -> dict:
    "run code user on container and return output"
    total_score, total_cases = await SandboxService.grade_code()
    return {"total_score": total_score, "total_cases": total_cases}

@router.get("/test-code-vm")
async def test_sandbox_container() -> dict:
    "run code user on container and return output"
    try:
        user_code = """a=input()\nb=input()\nprint(a, b)"""
        test_input = """2\n3"""

        if not user_code or not test_input:
            raise HTTPException(status_code=400, detail=MISSING_FIELD)

        output, error = await SandboxService.run_code_in_docker(user_code, test_input)

        if error:
            raise HTTPException(status_code=400, detail=error)
        return {"output": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/submit", response_model=SubmitResponseAll)
async def python_sandbox_submit(sandbox_request: SandboxRequest
                                ) -> SubmitResponseAll:
    "this is python sandbox"
    return await SandboxService.submit(sandbox_request)
