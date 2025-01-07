import subprocess

from typing import Union
 
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root(sourceCode: str):
    try:
        # เขียน source code ลงไฟล์ชั่วคราว
        with open("temp_code.py", "w") as f:
            f.write(sourceCode)

        # รันไฟล์ด้วย subprocess
        result = subprocess.run(
            ["python", "temp_code.py"],
            capture_output=True,
            text=True,
        )
        if result.stdout:
            print("Output:")
            print(result.stdout)
        if result.stderr:
            print("Error:")
            print(result.stderr)
        
        return {"output": result.stdout}

    except Exception as e:
        return {"Error": e}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}