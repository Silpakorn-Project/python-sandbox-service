"Module"
import dataclasses
from typing import List
from pydantic import BaseModel

class TestCase(BaseModel):
    "TestCase"
    input: List[str]
    expect_output: List[str]

    @dataclasses.dataclass
    class Config:
        "Example"
        testcase = {
            "example": {
                "input": ["1", "2", "3"],
                "expect_output": ["2", "3", "4"],
            }
        }
