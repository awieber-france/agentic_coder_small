import os
import json
import sys
import argparse
from config import MAX_ITER_AGENT, TEMPERATURE
from dotenv import load_dotenv
from openai import OpenAI
import prompts
from call_function import available_functions, call_function


def main():
    args = cli_parser()

    #Initialize messages history
    system_prompt = prompts.system_prompt
    messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt}
        ]
    
    #Open chatbot client via API
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the .env file in main directory.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    #Print if verbose
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    #Run agent in loop
    for _ in range(MAX_ITER_AGENT):
        messages, job_done = generate_content(client, messages, args.verbose, TEMPERATURE)
        if job_done:
            print(messages[-1])
            sys.exit(0)

    #Failure to finish job, exit with code=1
    sys.exit(1)


def cli_parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args


def generate_content(client: OpenAI, messages: list, verbose: bool, temperature: float | None = None) -> None:
    #Initialize parameters
    job_done = False

    #Interact with chatbot
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            temperature = temperature,
            tools=available_functions,
        )
    if not response.usage:
        api_fail_message = {"role": "API", "content": "The API response appears to be malformed. Please try again."}
        messages.append(api_fail_message)
        if verbose:
            print(f'Error: {api_fail_message["content"]}')
        return messages, job_done
        #raise RuntimeError("API response appears to be malformed.")
    message = response.choices[0].message
    if message.content is not None:
        messages.append({"role": "assistant", "content": message.content})
    else:
        messages.append({"role": "assistant", "reasoning": message.reasoning})

    #Print results
    if verbose:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completion_tokens}")

    # Run tool calls (if there are any)
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            function_args = json.loads(tool_call.function.arguments or"{}")
            #print(f"Calling function: {tool_call.function.name}({function_args})")
            result_message = call_function(tool_call, verbose) #already formatted in {'role': 'tool', 'tool_call_id': STR, 'content': STR}
            messages.append(result_message)
            if verbose:
                print(f"-> {result_message['content']}")
        
    # If no tool calls, then append final LLM message into messages history and end agentic job
    else:
        print("Response:")
        print(message.content)
        messages.append({"role": "assistant", "content": message.content})
        job_done = True

    return messages, job_done

    


if __name__ == "__main__":
    main()