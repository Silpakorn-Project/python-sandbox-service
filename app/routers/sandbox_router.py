"Module FastApi"
import os
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse
from app.services.user_service import SandboxService
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

@router.post("/uploadfile")
async def upload_file(file: UploadFile = File(...)):
    "Test upload file"
    file_location = f"./uploads/{file.filename}"

    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    with open(file_location, "wb") as f:
        contents = await file.read()
        f.write(contents)

    return JSONResponse(content={"filename": file.filename,
                                 "size": len(contents), 
                                 "path": file_location})
