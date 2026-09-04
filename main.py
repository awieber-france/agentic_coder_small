"""
Launches an agentic AI. It is called via a command line interface (CLI) that takes a user prompt as the first and only argument. Verbose mode can be called through the CLI as well.
Launch the agent via the terminal (at root of project, with python env activated):
    python main.py [user_prompt] [--verbose]

Tools used by the AI are defined in functions.call_function.py. They manage read, write and execute operations on the machine.
See settings.py for the constraints applied to these operations and the agent.
"""


import os
import sys
import argparse
from time import sleep
from settings import MAX_ITER_AGENT, TEMPERATURE
from dotenv import load_dotenv
from openai import OpenAI
from util import prompts
from settings import MODEL
from functions.call_function import available_functions, call_function

def client_openai(api_key: str) -> OpenAI:
    return OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                )

def cli_parser():
    """
    Reads the input from the command line and transforms it into arguments
    """
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()

def generate_content(client: OpenAI, messages: list, verbose: bool, temperature: float | None = None) -> tuple[list, bool]:
    """
    Calls the LLM and gives access to tool calls
    Output: latest messages from LLM and job status
    """
    job_done = False

    # Interact with API
    try:
        response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature = temperature,
                tools=available_functions,
            )
    except Exception as e:
        if verbose:
            print(f"API request faile: {e}")
        api_fail_message = {"role": "user", "content": "[System Error: {e}. Please retry.]"}
        messages.append(api_fail_message)
        return messages, job_done

    # If API connection succeeds, then continue
    message = response.choices[0].message
    messages.append(message) # Append the raw response object directly to preserve tool_calls and metadata

    if verbose and response.usage:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    # Process tool calls if requested
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            messages.append(result_message)
            if verbose:
                print(f"-> {result_message.get('content')}")
    else:
        # No tool calls indicates completion
        if verbose:
            print(f"Response:\n{message.content}")
        job_done = True

    return messages, job_done

def main():
    """
    Launches LLM client and runs it through a loop, with message history updated at end of each loop.
    When iteration limit reached, a sys error is provided.
    Early exit if final result achieved before iteration limit.
    """
    #Open chatbot client via API
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the .env file in main directory.")
    client = client_openai(api_key)
    
    #Initialize messages history
    args = cli_parser()
    messages = [
            {"role": "system", "content": prompts.system_prompt},
            {"role": "user", "content": args.user_prompt}
        ]
    
    #Print if verbose
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")   

    #Run agent in loop
    for _ in range(MAX_ITER_AGENT):
        messages, job_done = generate_content(client, messages, args.verbose, TEMPERATURE)
        if job_done:
            final_message = messages[-1]
            final_text = getattr(final_message, "content", str(final_message))
            print(final_text)
            sys.exit(0) 

    #Failure to finish job, exit with code=1
    print("Agent reached maximumum iterations without finishing.")
    sys.exit(1)

if __name__ == "__main__":
    main()