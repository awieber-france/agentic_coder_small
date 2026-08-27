import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI


def main():
    args = cli_parser()

    #Initialize messages history
    messages = [
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

    generate_content(client, messages, args.verbose)


def cli_parser():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args


def generate_content(client: OpenAI, messages: list, verbose: bool) -> None:
    #Interact with chatbot
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
        )
    if not response.usage:
        raise RuntimeError("API response appears to be malformed.")

    #Print results
    if verbose:
        prompt_tokens = response.usage.prompt_tokens
        completion_tokens = response.usage.completion_tokens
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {completion_tokens}")
    print("Response:")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()