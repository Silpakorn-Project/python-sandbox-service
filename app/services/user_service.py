import asyncio
import subprocess
import os




class SandboxService:
    "this is sandbox service"
    @staticmethod
    async def run_user_code(user_code, test_input) -> str:
        "something."
        try:
            process = subprocess.run(
                ["python3", "-c", user_code],  
                input=test_input,
                text=True,
                capture_output=True,
                timeout=5,
                check=False
            )

            output = process.stdout.strip()
            error = process.stderr.strip()

            return output, error

        except subprocess.TimeoutExpired:
            return None, "Execution Timeout (5 seconds exceeded)"

    @staticmethod
    async def grade_code() -> str:
        "run all testcase"
        user_code = """x = int(input())\nprint(x * x)"""
        test_cases = [
            ("5\n", "25"),
            ("2\n", "4"),
            ("0\n", "0")
        ]
        total_score = 0
        for i, (test_input, expected_output) in enumerate(test_cases):
            output, error = await SandboxService.run_user_code(user_code, test_input)

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
        "run code on container"
        PATH_SUBMISSION = f"{os.getcwd()}/sandbox" if os.getenv("PATH_SUBMISSION") is None else os.getenv("PATH_SUBMISSION") 
        IMAGE_DOCKER = "python-sandbox:latest" if os.getenv("IMAGE_DOCKER") is None else os.getenv("IMAGE_DOCKER") 

        filename = "./sandbox/user_code.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(user_code2)

        try:
            process = await asyncio.to_thread(subprocess.run,
                [
                    "docker", "run", "--rm",
                    "--memory=50m",
                    "--cpus=0.5",
                    "-v", f"{PATH_SUBMISSION}:/sandbox",
                    f"{IMAGE_DOCKER}",
                    "bash", "-c", f"echo '{test_input2}' | python /sandbox/user_code.py"
                ],
                text=True,
                capture_output=True,
                timeout=10
            )

            return process.stdout.strip(), process.stderr.strip()

        except subprocess.TimeoutExpired:
            return None, "Execution Timeout (10 seconds exceeded)"

        finally:
            if os.path.exists(filename):
                print(filename)
                # os.remove(filename)