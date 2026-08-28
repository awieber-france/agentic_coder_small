import sys
from pathlib import Path
import utils
from functions.get_target_path import get_target_path_READ_secure
from get_sandboxed_path import get_sandboxed_READ_path

#LLM schema - the undeclared working_directory parameter is reserved for the programmer
schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

# Collect information on files withing the target directory (name, size, is_dir)
def get_files_info(working_directory: str | Path, directory: str = ".") -> str:
    # GET TARGET PATH (checking for permissions)
    target_path = get_target_path_READ_secure(working_directory, directory)
    # A string is an error message, a Path object is a valid target_path
    if isinstance(target_path, str):
        return utils.error_message_generic(target_path) 
    if not isinstance(target_path, Path):
        return utils.error_message_bad_path_object
    # GET FILES INFO
    try:
        #Must be directory
        if not target_path.is_dir():
            return utils.error_message_not_dir(directory)
        #Iterate on directory contents
        dir_contents = []
        for item in target_path.iterdir():
            is_dir = item.is_dir()
            try:
                size = item.stat().st_size if item.is_file() else 0 #Can fail if broken symlink
            except:
                size = 0
            dir_contents.append(f"{item.name}: file_size={size} bytes, is_dir={is_dir}") 
        #Format and return results as string
        content = "\n".join([f"  - {str(x)}" for x in dir_contents]) #Structure directory contents as a textual list of items
        return utils.success_message_with_header_DIR(directory, content)
    except Exception as e:
        return utils.error_message_generic_with_header(directory, e) # the error generator sanitizes the exception

if __name__ == "__main__":
    #All cases to test:
    working_directory = "calculator"
    target_directories = [".", "pkg", "/bin", "../", "main.py", "pkg -> /etc"]

    #Get raw string argument from launch.json debugger
    raw_arg = sys.argv[1] if len(sys.argv) > 1 else "False"
    #Check for values that should count as "True"
    run_cases = raw_arg.lower() in ("true", "yes", "oui", "t", "1")

    #Run debugger
    if run_cases is True:
        for dir in target_directories:
            result = get_files_info(working_directory, dir)
            print(result)