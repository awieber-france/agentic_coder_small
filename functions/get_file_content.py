import sys
from pathlib import Path
import utils
from config import MAX_CHARS, BASE_DIR
from functions.get_target_path import get_target_path_READ_secure

def get_file_content(working_directory: str, file_path: str, MAX_CHARS: int = MAX_CHARS) -> str:
    # READ ONLY PRIVELEDGES
    target_path = get_target_path_READ_secure(working_directory, file_path)
    if isinstance(target_path, str):
            return utils.error_message_generic(target_path) 
    if not isinstance(target_path, Path):
        return utils.error_message_bad_path_object(working_directory)
    # GET FILE INFO
    try:
        # Must be file
        if target_path.is_dir():
            return utils.error_message_not_file(file_path)
        # Read contents
        with open(target_path, "r", encoding="utf-8", errors="replace") as f:
            f_contents = f.read(MAX_CHARS)
            #If more chars remain, then file truncated
            if f.read(1):
                f_contents += utils.truncate_message(file_path, MAX_CHARS)
        return utils.success_message_with_header_FILE(file_path, f_contents)
    except Exception as e:
        #e = f'Error: File not found or is not a regular file: "{file_path}"'
        return utils.error_message_generic_with_header(target_path, e) #the error generator sanitizes the exception

if __name__ == "__main__":
    #All cases to test:
    working_directory = "calculator"
    file_paths = [".", "pkg", "/bin", "../", "main.py", "pkg -> /etc", "lorem.txt"]

    #Get raw string argument from launch.json debugger
    raw_arg = sys.argv[1] if len(sys.argv) > 1 else "False"
    #Check for values that should count as "True"
    run_cases = raw_arg.lower() in ("true", "yes", "oui", "t", "1")

    #Run debugger
    if run_cases is True:
        for file_path in file_paths:
            result = get_file_content(working_directory, file_path)
            print(result)