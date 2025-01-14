"Handle Error"

class CustomError(Exception):
    "Custom Error"
    def __init__(self, error_code: int, message: str):
        self.error_code = error_code
        self.message = message

class ItemNotFound(CustomError):
    "Item not found"
    def __init__(self, error_code, message):
        super().__init__(error_code, "Item" + message)
