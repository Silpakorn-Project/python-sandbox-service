"Module"
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")
class BaseResponse(BaseModel, Generic[T]):
    "BaseResponse"
    status: int
    message: Optional[str] = None
    data: Optional[T] = None

class TestCaseResponse(BaseModel):
    "TestCaseResponse"
    testcase_total: int
    testcase_correct: int
    testcase_wrong: int
