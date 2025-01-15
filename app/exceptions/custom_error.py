"Handle Error"
from starlette import status

class CustomError(Exception):
    "Custom Error"
    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return f"[Error {self.error_code}] {self.message}"

class MissingRequiredArgumentsException(CustomError):
    "MissingRequiredArgumentsException"
    def __init__(self, message):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY,
                         f"{message} required arguments are missing.")
