import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Project Root
READ_PERMITTED_DIR = "calculator"
WRITE_PERMITTED_DIR = "calculator"
FORBIDDEN_READ_PATHS = []
FORBIDDEN_WRITE_PATHS = ["functions", ".vscode", ".venv", "__pycache__"]
WRITE_PERMITTED_FILE_TYPES = [".txt", ".py", ".md"]
EXECUTE_PERMITTED_FILE_TYPES = [".py"]
MAX_CHARS = 10000
SUBPROC_TIMEOUT = 30 #in seconds


HEADER_DIR_RESULT = "Results for '{working_directory}' directory:\n"
HEADER_FILE_RESULT = "Contents of file '{file_path}':\n"
err_text = "Error: "
suc_text = "Success: "