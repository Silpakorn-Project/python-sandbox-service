from pydantic import BaseModel
# this is model in spring boot
# same as spring boot but i will call this Schema
class UserModel(BaseModel):
    id: int
    name: str
    email: str

class NumberModel(BaseModel):
    number1: int
    number2: int
