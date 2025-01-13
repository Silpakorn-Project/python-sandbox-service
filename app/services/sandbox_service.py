"Normally Module"
import asyncio
import logging
import subprocess
import os
from typing import Tuple
import uuid

from fastapi import HTTPException
from app.schemas.request_schema import TestCaseRequest
from app.schemas.response_schema import BaseResponse, TestCaseResponse

class SandboxService:
    "this is sandbox service"
    @staticmethod
    async def run_user_code(user_code, test_input) -> Tuple[str, str]:
        """
        The run_user_code function executes user-provided Python code using subprocess.run, 
        captures the output and errors, and handles timeouts gracefully.
        """
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
    async def grade_code() -> Tuple[int, int]:
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
    async def run_code_in_docker(user_code2: str, test_input2: str) -> Tuple[str, str]:
        "run code on container"
        path_submission = os.getenv("PATH_SUBMISSION") or f"{os.getcwd()}/sandbox"
        image_docker = os.getenv("IMAGE_DOCKER") or "python-sandbox:latest"

        folder_name = "./sandbox"
        filename = os.path.join(folder_name, "user_code.py")

        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        with open(filename, "w", encoding="utf-8") as f:
            f.write(user_code2)

        try:
            process = await asyncio.to_thread(subprocess.run,
                [
                    "docker", "run", "--rm",
                    "--memory=50m",
                    "--cpus=0.5",
                    "-v", f"{path_submission}:/sandbox",
                    f"{image_docker}",
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
                os.remove(filename)


    @staticmethod
    async def submit(user_request_sandbox: TestCaseRequest = None
        ) -> BaseResponse[TestCaseResponse]:
        "Process file and test case."
        try:
            if user_request_sandbox is None:
                raise ValueError("Test case data is required.")

            if (not user_request_sandbox.file and
                not user_request_sandbox.input and
                not user_request_sandbox.expect_output):
                raise ValueError("All data is required")

            if len(user_request_sandbox.input) != len(user_request_sandbox.expect_output):
                raise ValueError("Error server compute")

            return await SandboxService.run_test(user_request_sandbox)

        except ValueError as ve:
            logging.error("Validation error: %s", ve)
            raise HTTPException(status_code=400, detail=str(ve)) from ve
        except Exception as e:
            logging.exception("An unexpected error occurred.")
            raise HTTPException(status_code=500, detail="Internal Server Error") from e

    @staticmethod
    async def run_test(user_request_sandbox: TestCaseRequest) -> BaseResponse[TestCaseResponse]:
        "run code on container"
        path_submission = os.getenv("PATH_SUBMISSION") or f"{os.getcwd()}/sandbox"
        image_docker = os.getenv("IMAGE_DOCKER") or "python-sandbox:latest"

        test_case_total = len(user_request_sandbox.input)
        test_case_correct = 0
        test_case_wrong = 0

        for input_, expect_output in zip(user_request_sandbox.input,
                                         user_request_sandbox.expect_output):

            folder_name = "./sandbox"
            unique_filename = f"{uuid.uuid4()}.py"
            unique_filename_path = os.path.join(folder_name, unique_filename)

            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)

            content_file = user_request_sandbox.file
            with open(unique_filename_path, "w", encoding="utf-8") as f:
                f.write(content_file)

            try:
                process = await asyncio.to_thread(subprocess.run,
                    [
                        "docker", "run", "--rm",
                        "--memory=50m",
                        "--cpus=0.5",
                        "-v", f"{path_submission}:/sandbox",
                        f"{image_docker}",
                        "bash", "-c", f"echo '{input_}' | python /sandbox/{unique_filename}"
                    ],
                    text=True,
                    capture_output=True,
                    timeout=10
                )

                found_output, error = process.stdout.strip(), process.stderr.strip()

                if error:
                    test_case_wrong += 1
                    logging.error("Error while executing code: %s", error)
                    continue

                if found_output == expect_output:
                    test_case_correct += 1
                else:
                    test_case_wrong += 1

            except subprocess.TimeoutExpired:
                # return None, "Execution Timeout (10 seconds exceeded)"
                logging.error("Test case execution timed out (10 seconds exceeded).")
                test_case_wrong += 1

            finally:
                if os.path.exists(unique_filename_path):
                    print(unique_filename_path)
                    os.remove(unique_filename_path)

        return BaseResponse(
            status=200,
            message="something",
            data=TestCaseResponse(
                testcase_total=test_case_total,
                testcase_correct=test_case_correct,
                testcase_wrong=test_case_wrong,
            )
        )
