"""
Runs the functions called by the agent via its tool calls.
"""

import json
from util import utils
from collections.abc import Callable
from settings import WRITE_PERMITTED_DIR, READ_PERMITTED_DIR
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

def call_function(tool_call, verbose: bool = False) -> dict:
    """
    Runs a tool if the LLM provided the proper call.
    The permitted working directory is given here and depends on if the tool is read or write (execute is considered 'write')
    """
    try:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments or "{}")

        # Print the function to be called
        if verbose:
            print(f" - Calling function: {function_name}({function_args})")
        else:
            print(f" - Calling function: {function_name}")

        function_map: dict[str, Callable[..., str]] = {
            "get_file_content": get_file_content,
            "get_files_info": get_files_info,
            "run_python_file": run_python_file,
            "write_file": write_file,
        }

        # Return error if an unknown function is called
        if function_name not in function_map.keys():
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: Unknown function: {function_name}",
            }
        # READ OPERATIONS
        if function_name in ["get_files_info", "get_file_content"]:
            working_directory = READ_PERMITTED_DIR
            result = function_map[function_name](working_directory, **function_args)
        # WRITE AND EXECUTE OPERATIONS
        if function_name in ["run_python_file", "write_file"]:
            working_directory = WRITE_PERMITTED_DIR
            result = function_map[function_name](working_directory, **function_args)
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        }
    except Exception as e:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": utils.error_message_generic(e),
        }