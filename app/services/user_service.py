import asyncio
import subprocess
import os
import uuid


user_code = """
x = int(input())
print(x * x)
"""

test_cases = [
    ("5\n", "25"),   # Input: 5, Expected Output: 25
    ("2\n", "4"),    # Input: 2, Expected Output: 4
    ("0\n", "0")     # Input: 0, Expected Output: 0
]

class UserService:
    @staticmethod
    async def getUsers() -> str:
        return "test" 

    @staticmethod
    async def run_user_code(user_code, test_input) -> str:
        try:
        # รันโค้ดผู้ใช้ใน subprocess
            process = subprocess.run(
                ["python3", "-c", user_code],  # รันโค้ดใน Python
                input=test_input,             # ส่ง input ให้กับโค้ดผู้ใช้
                text=True,
                capture_output=True,          # เก็บผลลัพธ์จาก stdout และ stderr
                timeout=5                     # จำกัดเวลาในการรัน (5 วินาที)
            )

            # เก็บผลลัพธ์
            output = process.stdout.strip()
            error = process.stderr.strip()
            return output, error

        except subprocess.TimeoutExpired:
            return None, "Execution Timeout (5 seconds exceeded)"

    @staticmethod
    async def grade_code() -> str:
        total_score = 0
        for i, (test_input, expected_output) in enumerate(test_cases):
            output, error = await UserService.run_user_code(user_code, test_input)

            print(f"Test Case {i+1}: Input: {test_input}")
            if error:
                print(f"Error: {error}")
            elif output == expected_output:
                print(f"Passed: Output = {output}")
                total_score += 1
            else:
                print(f"Failed: Output = {output}, Expected = {expected_output}")

        return total_score, len(test_cases)


    @staticmethod
    async def run_code_in_docker(user_code2: str, test_input2: str):
        # สร้างไฟล์โค้ดผู้ใช้
        print(os.getcwd())
        # filename = f"user_code_{uuid.uuid4().hex[:8]}.py"
        filename = f"./sandbox/user_code.py"
        with open(filename, "w") as f:
            f.write(user_code2)

        try:
            # รัน Docker Container พร้อม Mount โค้ดผู้ใช้
            # process = await asyncio.to_thread(subprocess.run,  # ใช้ asyncio เพื่อรัน subprocess แบบ non-blocking
            #     [
            #         "docker", "run", "--rm",
            #         "--memory=50m",  # จำกัด Memory (50MB)
            #         "--cpus=0.5",    # จำกัด CPU (0.5 Core)
            #         "-v", f"{os.getcwd()}/sandbox:/sandbox",  # Mount โฟลเดอร์ปัจจุบันเข้า Docker
            #         "python-sandbox",  # Docker Image ที่คุณสร้าง
            #     ],
            #     input=test_input2,        # ส่ง Input เข้า Docker
            #     text=True,
            #     capture_output=True,     # เก็บผลลัพธ์และ Error
            #     timeout=10               
            # )

            #if you use asyncio.to_thread you must manage stdin 
            #fix stdin
            process = await asyncio.to_thread(subprocess.run,
                [
                    "docker", "run", "--rm",
                    "--memory=50m",
                    "--cpus=0.5",
                    "-v", f"{os.getcwd()}/sandbox:/sandbox",
                    "python-sandbox",
                    "bash", "-c", f"echo '{test_input2}' | python /sandbox/user_code.py"
                ],
                text=True,
                capture_output=True,
                timeout=10
            )


            # คืนผลลัพธ์
            return process.stdout.strip(), process.stderr.strip()

        except subprocess.TimeoutExpired:
            return None, "Execution Timeout (10 seconds exceeded)"

        finally:
            # ลบไฟล์โค้ดผู้ใช้หลังรันเสร็จ
            if os.path.exists(filename):
                print(filename)
                # os.remove(filename)




