import utils
from config import SUBPROC_TIMEOUT
from pathlib import Path
import subprocess
import sys
from functions.get_target_path import get_target_path_EXECUTE_secure

#LLM schema - the undeclared working_directory parameter is reserved for the programmer
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Allows execution of a python script within the working directory via a subprocess",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the python script to run via a subprocess, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list[string]",
                    "description": "Additional arguments to be used in the the python script at file_path",
                },
            },
        },
    },
}

#Executing a file requires write priveledges
def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        #Get target path checked for permissions
        target_path = get_target_path_EXECUTE_secure(working_directory, file_path)
        # If text, then it is an error message
        if isinstance(target_path, str):
            return utils.error_message_generic(target_path)
        # A correct target path is in the Path format
        if not isinstance(target_path, Path):
            return utils.error_message_bad_path_object(working_directory)

        #Run subprocess
        if not target_path.exists():
            return utils.error_message_execute_file_not_exist(file_path)
        command = ["python", target_path, *(args or [])]
        subproc = subprocess.run(command, capture_output=True, text=True, timeout=SUBPROC_TIMEOUT) #Capture both stdout and stderr in string form

        #Return outputs
        outputs = []
        if subproc.returncode != 0:
            outputs.append(f'Process exited with code {subproc.returncode}')
        stdout = subproc.stdout.strip() #strip trailing newlines/whitespace
        stderr = subproc.stderr.strip() #strip trailing newlines/whitespace
        if not stdout and not stderr:
            outputs.append("No output produced")
        else:
            if stdout:
                outputs.append(f"STDOUT: {stdout}")
            if stderr:
                outputs.append(f"STDERR: {stderr}")
        return " - ".join(outputs)
    except Exception as e:
        return utils.error_message_execute_filetype_invalid(e)

    

    #EXTEND PYTHON CALL WITH EXTRA ARGUMENTS IF INCLUDED

if __name__ == "__main__":
    #All cases to test:
    arg_combos = [["calculator", "main.py"],
                  ["calculator", "main.py", ["3 + 5"]],
                  ["calculator", "tests.py"],
                  ["calculator", "../main.py"],
                  ["calculator", "nonexistent.py"],
                  ["calculator", "lorem.txt"]
                  ]

    #Get raw string argument from launch.json debugger
    raw_arg = sys.argv[1] if len(sys.argv) > 1 else "False"
    #Check for values that should count as "True"
    run_cases = raw_arg.lower() in ("true", "yes", "oui", "t", "1")

    #Run debugger
    if run_cases is True:
        sys.argv[1] = "False" #DON'T RUN DEBUGGER IN OTHER FILES
        print("\nCASES TESTED:\n")
        for args in arg_combos:
            print(f'\nCase being tested: {args}')
            if len(args) < 2:
                result = "Error: subprocess failed to run because less than 2 arguments were supplied"
                continue
            result = run_python_file(*args)
            print(result)