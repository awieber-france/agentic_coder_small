from pathlib import Path
import utils
import sys
from config import BASE_DIR
from get_sandboxed_path import get_sandboxed_READ_path, get_sandboxed_WRITE_path

def get_target_path_READ_secure(working_directory: Path | str, directory: str = ".") -> Path | str:
    return _get_target_path_with_permission_check(working_directory, directory, write=False)

def get_target_path_WRITE_secure(working_directory: Path | str, directory: str = ".") -> Path | str:
    return _get_target_path_with_permission_check(working_directory, directory, write=True)

def _get_target_path_with_permission_check(working_directory: Path | str, directory: str = ".", write: bool = False) -> Path | str:
    """
    Returns a Path object for target_path (if authorized)
    Works for directories and files
    Otherwise returns the error as a string
    """
    #Get authorized read path
    if write:
        auth_path = get_sandboxed_WRITE_path() # If this fails, then the AI agent should hard crash
    else:
        auth_path = get_sandboxed_READ_path() # If this fails, then the AI agent should hard crash

    #Check for symlinks
    if _symlink_symbol(working_directory) or _symlink_symbol(directory):
        return utils.error_message_symlink_present(directory)
    
    #Get target path, checking for authorization
    try:
        #Resolve working and target directories completely
        workspace = Path(working_directory).resolve(strict=True)
        target_path = (workspace / directory).resolve(strict=False if write else True)
        #Check permissions
        if not target_path.is_relative_to(auth_path):
            return utils.error_message_dir_not_auth(directory)
        #Check if declared working directory is coherent with final target path
        if not target_path.is_relative_to(workspace):
            return utils.error_message_outside_working_dir(directory)
        #Prevent overwriting of existing directory
        if write and target_path.is_dir():
            return utils.error_message_overwrite_dir(directory)
    except Exception as e:
        return utils.error_message_generic_with_header(directory, e) # the error generator sanitizes the exception
    return target_path


def _symlink_symbol(path: str) -> bool:
    if "->" in path:
        return True
    else:
        return False

if __name__ == "__main__":
    #All cases to test:
    working_directory = "calculator"
    directories = [".", "pkg", "/bin", "../", "main.py", "pkg -> /etc"]

    #Get raw string argument from launch.json debugger
    raw_arg = sys.argv[1] if len(sys.argv) > 1 else "False"
    #Check for values that should count as "True"
    run_cases = raw_arg.lower() in ("true", "yes", "oui", "t", "1")

    #Run debugger
    if run_cases is True:
        print("\nREAD CASES TESTED:\n")
        for directory in directories:
            result = get_target_path_READ_secure(working_directory, directory)
            print(result)

        print("\nWRITE CASES TESTED:\n")
        for directory in directories:
            result = get_target_path_WRITE_secure(working_directory, directory)
            print(result)