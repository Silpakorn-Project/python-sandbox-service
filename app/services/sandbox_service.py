"Normally Module"
import asyncio
import logging
import subprocess
import os
from typing import List, Tuple
import uuid

from app.exceptions.custom_error import MissingRequiredArgumentsException
from app.schemas.request_schema import SandboxRequest
from app.schemas.response_schema import SubmitResponseAll, TestCaseResponse

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
            return "", "Execution Timeout (5 seconds exceeded)"

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
            return "", "Execution Timeout (10 seconds exceeded)"

        finally:
            if os.path.exists(filename):
                print(filename)
                os.remove(filename)


    @staticmethod
    async def submit(sandbox_request: SandboxRequest) -> SubmitResponseAll:
        """Process file and test case."""
        SandboxService.validate_request(sandbox_request)
        return await SandboxService.run_test(sandbox_request)

    @staticmethod
    def validate_request(sandbox_request: SandboxRequest):
        """Validate the sandbox request."""
        if sandbox_request.source_code is None or sandbox_request.source_code == "":
            raise MissingRequiredArgumentsException("Empty source.code")
        if (sandbox_request.test_cases is None
            or sandbox_request.test_cases == ""
            or len(sandbox_request.test_cases) == 0):
            raise MissingRequiredArgumentsException("Empty testcase")

    @staticmethod
    def create_file(content: str, folder_name: str, unique_filename: str) -> str:
        """Create a Python file with the given content."""
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        unique_filename_path = os.path.join(folder_name, unique_filename)
        with open(unique_filename_path, "w", encoding="utf-8") as f:
            f.write(content)
        return unique_filename_path

    @staticmethod
    def delete_file(file_path: str):
        """Delete a file."""
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def run_docker(image: str, path_submission: str,
                   unique_filename: str, test_input: str
                   ) -> subprocess.CompletedProcess:
        """Run the Docker container to execute the code."""
        return subprocess.run(
            [
                "docker", "run", "--rm", "--name", f"{unique_filename[:-3]}",
                "--memory=50m", "--cpus=0.5",
                "-v", f"{path_submission}:/sandbox",
                image,
                "bash", "-c", f"echo '{test_input}' | python /sandbox/{unique_filename}"
            ],
            text=True,
            capture_output=True,
            timeout=10,
            check=False
        )

    @staticmethod
    async def run_test(sandbox_request: SandboxRequest) -> SubmitResponseAll:
        """Run code on a container."""
        path_submission: str = os.getenv("PATH_SUBMISSION") or f"{os.getcwd()}/sandbox"
        image_docker: str = os.getenv("IMAGE_DOCKER") or "python-sandbox:latest"

        test_case_total: int = len(sandbox_request.test_cases)
        test_case_correct: int = 0
        test_case_wrong: int = 0
        test_cases_response: List[TestCaseResponse] = []
        is_all_passed: bool = True

        for test_case in sandbox_request.test_cases:
            folder_name = "./sandbox"
            unique_filename = f"{uuid.uuid4()}.py"
            unique_filename_path = SandboxService.create_file(sandbox_request.source_code,
                                                              folder_name,
                                                              unique_filename)

            try:
                process = await asyncio.to_thread(SandboxService.run_docker,
                                                  image_docker, path_submission,
                                                  unique_filename, test_case.input)
                actual_output, error = process.stdout.strip(), process.stderr.strip()

                if error:
                    test_cases_response.append(TestCaseResponse(
                        passed=False,
                        input=test_case.input,
                        expected=test_case.expected_output,
                        actual=actual_output,
                        error=error
                    ))
                    test_case_wrong += 1
                    is_all_passed = False
                elif actual_output == test_case.expected_output:
                    test_cases_response.append(TestCaseResponse(
                        passed=True,
                        input=test_case.input,
                        expected=test_case.expected_output,
                        actual=actual_output,
                        error=None
                    ))
                    test_case_correct += 1
                else:
                    test_cases_response.append(TestCaseResponse(
                        passed=False,
                        input=test_case.input,
                        expected=test_case.expected_output,
                        actual=actual_output,
                        error=None
                    ))
                    test_case_wrong += 1
                    is_all_passed = False

            except subprocess.TimeoutExpired:
                logging.error("Test case execution timed out (10 seconds exceeded).")
                test_cases_response.append(TestCaseResponse(
                    passed=False,
                    input=test_case.input,
                    expected=test_case.expected_output,
                    actual="",
                    error="Test case execution timed out (10 seconds exceeded)."
                ))
                test_case_wrong += 1
                is_all_passed = False

            finally:
                SandboxService.delete_file(unique_filename_path)
                try:
                    subprocess.run(
                        ["docker", "rm", "-f", f"{unique_filename[:-3]}"],
                        check=False,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                except subprocess.SubprocessError as e:
                    logging.error("Error while removing Docker container: %s", e)

        return SubmitResponseAll(
            testcase_total=test_case_total,
            testcase_passed=test_case_correct,
            testcase_wrong=test_case_wrong,
            passed=is_all_passed,
            test_cases=test_cases_response
        )
