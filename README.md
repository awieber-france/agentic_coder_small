# Agentic Coder (small)

**WARNING: Use at your own risk (any damage is your own responsability).**
<br>This agentic coder built entirely in Python is a case study, not a professional grade system applying all best security practices. The Agent can technically BREAK OUT by modifying python scripts within its working directory. To limit the risks, an iteration limit of 20 and a free LLM model (limits on daily tokens) is used. DO NOT give a user prompt that pushes the model to break out.

## Introduction
This case study uses a custom-built AI agent (LLM orchestrator and Python tools) to take a preexisting calculator python app and improve it / correct errors. As such, it has acces to read/write/execute functions within its working directory. These tools allow for iterative adjustments and error corrections on this calculator app. If it is asked to work on something other than the calculator app, then it will attempt to do it.

The agent can also respond to questions without using any read/write/execute tools.

NOTE: The calculator is Python code that takes simple arithmetic equations supplied as a string (ex: 4 + 3 * 20 - 1 / 2). This is executed through a command line interface (CLI) where the first argument is the mathematical equation. Parentheses are not accepted.

## Details of AI priveledges

Priveledges provided to the AI Agent are:
- **Read:** project subdirectory, all file types
- **Overwrite:** project subdirectory, file types {.txt, .py, .md}
- **Write new file:** project subdirectory, file types {.txt, .md}
- **Run executable:** project subdirectory, file types {.py}

The project subdirectory is set to ***'Calculator'***.

Since the agent can modify executables (python files within the project subdirectory, it is dangerous)

The following is verified during working directory validation:
- No symlinks
- The path is a Path object from pathlib (always resolved)
- The working directory is relative to the project directory
- The working directory is relative to the *permitted* working directory as defined in *settings.py*
- Write operations are not performed on a directory
- File is of permitted file type

## Suggested test case
**Quick test:**

Run the agent via the following command:
- python main.py "Does the calculator in this project give the correct answer for '3 + 4 * 2'?"

**Testing of code correction capabilities:**

Perform the following steps:
- modify the *calculator/pkg/calculator.py* code so that the '+' operation has a precedence of 3.
- run the agent via the following command:
   - python main.py "The calculator in this project gives me the wrong result for '3 + 4 * 2. Please diagnose and correct the problem. Tell me what was wrong, what you did, and what the final result is after the fixes."

## Requirements

The environment manager ***uv*** was used to create and run the project. All dependencies are saved in the requirements.txt file.

**Python version tested:** 3.11.5