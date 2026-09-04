from pathlib import Path
import sys
from settings import BASE_DIR, READ_PERMITTED_DIR, WRITE_PERMITTED_DIR, FORBIDDEN_READ_PATHS, FORBIDDEN_WRITE_PATHS

# NOT GUARANTEED TO BE SANDBOXED. PYTHON IS NOT SECURE FOR THIS, BUT THIS IS A CASE STUDY. BEST ATTEMPT MADE TO SECURE IT.
# EXECUTABLES AND SCRIPTS SHOULD BE PROTECTED INDIVIDUALLY ON THE OPERATING SYSTEM TO HELP MINIMIZE BREAKOUT RISKS.

def _get_sandboxed_BASE_path() -> Path:
    """
    Takes hardcoded directory declaration for the base directory and returns a Path object.
    If this function fails, then the AI agent should not even run.
    """
    # 1. Canonicalize base directory (strict=True ensures the base folder exists)
    base_path = Path(BASE_DIR).resolve(strict=True)
    return base_path

def _validate_permitted_dir(permitted_dir_name: str, forbidden_dirs: list[str], disallow_base: bool = True) -> Path:
    """
    Check read or write paths for permissions (generically named target_path).
    Forbidden directories are verified. The target path cannot be inside (or equal) to any forbidden directory.
    Inversely, a forbidden directory inside the target path is unauthorized.
    If this function fails, then the AI agent should not even run.
    """
    # 1. Get base directory from secure, sandboxed function
    base_path = _get_sandboxed_BASE_path()
    # 2. Combine and fully resolve target_path (collapses '..', '.', and all symlinks)
    target_path = (base_path / permitted_dir_name).resolve()
    # 3. Validate existence of directory
    if not target_path.exists():
        raise FileNotFoundError(f"Error: permitted path '{target_path}' does not exist.")
    # 4. Validate that path is a directory
    if not target_path.is_dir():
        raise NotADirectoryError(f"Error: permitted path '{target_path}' is not a directory.")
    # 5. Check structural boundary containment (within project workspace)
    if not target_path.is_relative_to(base_path):
        raise PermissionError(f"Error: permitted path '{target_path}' is outside project workspace.")
    # 6. Ensure that target path is never the base path (for write_path) - FIRST CONDITION TO ELIMINATE?
    if disallow_base and target_path == base_path:
        raise PermissionError("Error: write access to the project root is forbidden.")
    # 7. Ensure target_path does not overlap with any forbidden directory
    for forb_dir in forbidden_dirs:
        forbidden_path = (base_path / forb_dir).resolve()
        if target_path.is_relative_to(forbidden_path):
            raise PermissionError(f"Error: Permitted path '{target_path}' is inside forbidden directory '{forbidden_path}'.")
        if forbidden_path.is_relative_to(target_path):
            raise PermissionError(f"Error: Permitted path '{target_path}' contains forbidden directory '{forbidden_path}'.")
    return target_path

def get_sandboxed_READ_path() -> Path:
    return _validate_permitted_dir(READ_PERMITTED_DIR, FORBIDDEN_READ_PATHS, disallow_base=True)

def get_sandboxed_WRITE_path() -> Path:
    return _validate_permitted_dir(WRITE_PERMITTED_DIR, FORBIDDEN_WRITE_PATHS, disallow_base=True)


if __name__ == "__main__":
    #Get raw string argument from launch.json debugger
    raw_arg = sys.argv[1] if len(sys.argv) > 1 else "False"
    #Check for values that should count as "True"
    run_debug = raw_arg.lower() in ("true", "yes", "oui", "t", "1")

    #Run debugger
    if run_debug is True:
        print("\nRunning get_sandboxed_READ_path:\n")
        result = get_sandboxed_READ_path()
        print(result)

        print("\nRunning get_sandboxed_WRITE_path:\n")
        result = get_sandboxed_WRITE_path()
        print(result)