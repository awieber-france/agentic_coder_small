from pathlib import Path
from functions.get_target_path import get_target_path_WRITE_secure
from get_sandboxed_path import get_sandboxed_WRITE_path, _get_sandboxed_BASE_path
import utils
import sys

def write_file(working_directory: str, file_path: str, content: str) -> str:
    # WRITE PRIVELEDGES
    target_path = get_target_path_WRITE_secure(working_directory, file_path)
    # If text, then it is an error message
    if isinstance(target_path, str):
        return utils.error_message_write_fail(target_path)
    # A correct target path is in the Path format
    if not isinstance(target_path, Path):
        return utils.error_message_bad_path_object(working_directory)
    
    # DOUBLE CHECK WRITE PRIVELEDGES
    if not target_path.is_relative_to(get_sandboxed_WRITE_path()) and not target_path.is_relative_to(_get_sandboxed_BASE_path()):
          return utils.error_message_dir_not_auth(file_path)
    
    # Write file
    try:
        #------WRITE ACTION NOT ACTIVATED YET (CODE IN TESTING)-------
        with open(target_path, "w", encoding="utf-8", errors="replace") as f:
              f.write(content)
        return utils.success_message_WRITE(file_path, content)
        #return f"Results for '{file_path}':\n  WARNING: Writing not yet implemented, but would have attempted to write to '{file_path}' - content to write:\n{content}"
    except Exception as e:
         return utils.error_message_generic(e) #the error generator sanitizes the exception

if __name__ == "__main__":
    work_dir = "calculator"
    file_paths = ["lorem_test.txt",
                  "pkg/morelorem.txt",
                  "/tmp/temp.txt"]
    content = ["wait, this isn't lorem ipsum (written directly from the in debugging mode)",
               "lorem ipsum dolor sit amet (written directly from the in debugging mode)",
               "this should not be allowed (written directly from the in debugging mode)"]

    #Get raw string argument from launch.json debugger
    raw_arg = sys.argv[1] if len(sys.argv) > 1 else "False"
    #Check for values that should count as "True"
    run_cases = raw_arg.lower() in ("true", "yes", "oui", "t", "1")

    #Run debugger
    if run_cases is True: 
        for file_path, content in zip(file_paths, content):
            result = write_file(work_dir, file_path, content)
            print(result)