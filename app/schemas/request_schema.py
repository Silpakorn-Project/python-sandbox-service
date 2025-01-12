"Module"
from typing import List
from pydantic import BaseModel

class TestCaseRequest(BaseModel):
    "TestCase Request Model"
    file: str
    input: List[str]
    expect_output: List[str]

    class Config:
        "Example"
        schema_extra = {
            "example": {
                "file": "print(int(input())+1)",
                "input": ["1"],
                "expect_output": ["2"],
            }
        }
