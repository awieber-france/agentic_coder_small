from pathlib import Path
from functions.get_target_path import get_target_path_WRITE_secure
from get_sandboxed_path import get_sandboxed_WRITE_path, _get_sandboxed_BASE_path
import utils

def write_file(working_directory: str, file_path: str, content: str) -> str:
    # WRITE PRIVELEDGES
    target_path = get_target_path_WRITE_secure(working_directory, file_path)
    # If text, then it is an error message
    if isinstance(target_path, str):
        return utils.error_message_bad_file(target_path)
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
     #file_paths = [".", "pkg", "/bin", "../", "main.py", "pkg -> /etc", "lorem.txt", "/tmp/temp.txt"]
     file_paths = ["lorem_test.txt", "pkg/morelorem.txt", "/tmp/temp.txt"]
     content = "This is text written by the write_file function."

     for file_path in file_paths:
        result = write_file(work_dir, file_path, content)
        print(result)