"Module"
from typing import Optional, List
from pydantic import BaseModel

class TestCaseResponse(BaseModel):
    "TestCaseResponse"
    passed: bool
    input: str
    expected: str
    actual: str
    error: Optional[str]

class SubmitResponseAll(BaseModel):
    "BaseResponse"
    testcase_total: int
    testcase_passed: int
    testcase_wrong: int
    passed: bool
    test_cases: List[TestCaseResponse]
