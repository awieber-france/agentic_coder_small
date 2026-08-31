import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Project Root
READ_PERMITTED_DIR = "calculator" #Working directory for read operations (permission given only for this and its subdirs)
WRITE_PERMITTED_DIR = "calculator" #Working directory for write/execute operations (permission given only for this and its subdirs)
FORBIDDEN_READ_PATHS = [] #Banned directories for write ops (relative to BASE_DIR)
FORBIDDEN_WRITE_PATHS = ["functions", ".vscode", ".venv", "__pycache__"] #Banned directories for write ops (relative to BASE_DIR)
CREATE_PERMITTED_FILE_TYPES = [".txt", ".md"]
WRITE_PERMITTED_FILE_TYPES = [".txt", ".py", ".md"] #Types of files that can be written by the scripts / LLM
EXECUTE_PERMITTED_FILE_TYPES = [".py"] #Types of files that can be executed by the scripts / LLM
MAX_CHARS = 10000 #Max characters before truncation when getting content of a file
SUBPROC_TIMEOUT = 30 #in seconds    #Timeout when a python function calls another function via a subprocess
MAX_ITER_AGENT = 20 #Maximum iterations allowed for the agent (number of generate_content calls)
TEMPERATURE = 0 #Temperature to use for all LLM responses