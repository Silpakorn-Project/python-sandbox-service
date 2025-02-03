"Module"
import dataclasses
from typing import List
from pydantic import BaseModel

class TestCaseRequest(BaseModel):
    "TestCase Request Model"
    input: str
    expected_output: str

class SandboxRequest(BaseModel):
    "Sandbox Request Model"
    source_code: str
    test_cases: List[TestCaseRequest]

    @dataclasses.dataclass
    class Config:
        "Example"
        json_schema_extra = {
            "example": {
                "source_code": "print(int(input())+1)",
                "test_cases": [
                    {
                        "input": "1",
                        "expected_output": "2"
                    },
                    {
                        "input": "2",
                        "expected_output": "3"
                    }
                ]
            }
        }
