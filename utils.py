from config import HEADER_DIR_RESULT, HEADER_FILE_RESULT, MAX_CHARS, BASE_DIR
from pathlib import Path

def sanitize_exception(exc: Exception, workspace_root: str | Path) -> str:
    """Replaces absolute workspace path in exception strings with relative paths."""
    try:
        error_str = str(exc)
        if isinstance(workspace_root, str):
            abs_root = workspace_root
        elif isinstance(workspace_root, Path):
            abs_root = str(workspace_root.resolve())
        else:
            return unknown_path_error()
        
        # Replace the absolute workspace root path with standard relative path marker
        if abs_root in error_str:
            error_str = error_str.replace(abs_root, ".")
    except:
        return unknown_path_error()
    return error_str

# Usage Example:
# Input:  [Errno 2] No such file or directory: '/Users/jsmith/Documents/.../calculator/pkg/does_not_exist.py'
# Output: [Errno 2] No such file or directory: './calculator/pkg/does_not_exist.py'

def format_header_dir(working_directory):
    return HEADER_DIR_RESULT.format(working_directory=working_directory)

def format_header_file(file_path):
    return HEADER_FILE_RESULT.format(file_path=file_path)

#HEADER for messages (success or error)
header_template_DIR = "Results for '{target_directory}' directory:\n"
header_template_FILE = "Results for '{target_directory}' file:\n"
header_template_GENERIC = "Results for '{target_directory}':\n"

def get_header(target: str, type: str) -> str:
    if type == "DIR":
        return header_template_DIR.format(target_directory=target)
    elif type == "FILE":
        return header_template_FILE.format(target_directory=target)
    else:
        return header_template_GENERIC.format(target_directory=target)

#WRITE failure message to append
def write_fail_message_to_append():
    return " - write attempt failed"

#SUCCESS messages (templates)
def success_message_with_header_DIR(target: str, content: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}{content}'

def success_message_with_header_FILE(target:str, content: str):
    header = header_template_FILE.format(target_directory=target)
    return f'{header}{content}'

def success_message_with_header_WRITE(target: str, content: str):
    header = header_template_FILE.format(target_directory=target)
    return f'{header}Successfully wrote to "{target}" ({len(content)} characters written)'

#TRUNCATE string (truncates read output when too long)
def truncate_message(target: str, chars: int = MAX_CHARS):
    return f'[...File "{target}" truncated at {chars} characters]'

#ERROR messages (templates):
def unknown_path_error():
    return f'Error: unkown failure with path' #useful when the full error message would leak information compromising security

def error_message_generic(exception_message: str):
    exc_sanitized = sanitize_exception(exception_message, BASE_DIR)
    return exc_sanitized

def error_message_generic_with_header(target: str, exception_message: str):
    header = header_template_DIR.format(target_directory=target)
    exc_sanitized = sanitize_exception(exception_message, BASE_DIR)
    return f'{header}  Error: {exc_sanitized}'

def error_message_bad_path_object(target: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}  Error: could not resolve directory "{target}" as a Path object.'

def error_message_not_dir(target: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}  Error: "{target}" is not a directory'

def error_message_outside_working_dir(target: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}  Error: "{target}" is outside the declared working directory'

def error_message_dir_not_auth(target: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}  Error: permission denied to "{target}" directory'

def error_message_symlink_present(target: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}  Error: banned symlink symbol "->" used in path'

def error_message_not_file(target: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}  Error: "{target}" is not a file'

def error_message_overwrite_dir(target: str):
    header = header_template_DIR.format(target_directory=target)
    return f'{header}  Error: Cannot write to "{target}" as it is an existing directory (overwrite of directories not authorized)' 