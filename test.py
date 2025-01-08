import subprocess

def run_user_code(user_code, test_input):
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

def grade_code(user_code, test_cases):
    total_score = 0
    for i, (test_input, expected_output) in enumerate(test_cases):
        output, error = run_user_code(user_code, test_input)

        print(f"Test Case {i+1}: Input: {test_input}")
        if error:
            print(f"Error: {error}")
        elif output == expected_output:
            print(f"Passed: Output = {output}")
            total_score += 1
        else:
            print(f"Failed: Output = {output}, Expected = {expected_output}")

    return total_score, len(test_cases)

# ตัวอย่าง Test Cases
test_cases = [
    ("5\n", "25"),   # Input: 5, Expected Output: 25
    ("2\n", "4"),    # Input: 2, Expected Output: 4
    ("0\n", "0")     # Input: 0, Expected Output: 0
]

# โค้ดตัวอย่างของผู้ใช้ (สมมติว่าให้ยกกำลัง 2)
user_code = """
x = int(input())
print(x * x)
"""

# รัน Grader
score, total = grade_code(user_code, test_cases)
print(f"Final Score: {score}/{total}")
