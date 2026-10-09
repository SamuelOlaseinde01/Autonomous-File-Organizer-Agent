import argparse
import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from functions.call_function import available_tools, call_function


def main():
    try:
        load_dotenv()

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY")
        )


        parser = argparse.ArgumentParser()
        parser.add_argument("user_prompt", type=str, help="The prompt of the user")
        parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
        args = parser.parse_args()

        user_prompt = args.user_prompt
        system_prompt = """
        You are a highly efficient, logical File Organization Assistant. Your sole objective is to clean, restructure, and organize a user's digital file environment.

        Objectives:
        1. Analyze existing files and directories to understand their contents, file types, and current context.
        2. Group files into logical categories (by project, topic, file type, or date) depending on user instructions or clear logical patterns.
        3. Execute organization plans systematically using the minimal number of tool steps required.

        Guidelines & Rules:
        - Look Before You Leap: Always gather data first using `get_files_info` if you do not know the exact file names or directory layouts.
        - Incremental Steps: Execute your plan sequentially. For example, you must create a folder using `create_folder` before attempting to use `move_file` to send files into it.
        - Aesthetic & Order: Avoid generic folder names. Opt for clear, lowercase-with-underscores or PascalCase naming conventions (e.g., `invoices_2026`, `Project_Alpha`).
        - No Assumptions: If a file's category is entirely ambiguous, leave it in place or ask for user clarification instead of guessing a wrong location.

        You must choose the single best tool from your available tools for your immediate next step. Do not invent or assume other actions exist.
        """
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {    
                "role": "user",
                "content": user_prompt
            },
        ] 
        
        final_response_message = None
        
        for _ in range(20):
            response = client.chat.completions.create(
                model="openrouter/free",
                messages=messages,
                tools=available_tools
            )
            
            message = response.choices[0].message
                           
            if message.tool_calls:    
                messages.append(message.model_dump())
                for tool_call in message.tool_calls:
                    result_message = call_function(tool_call, args.verbose)
                    if not result_message["content"]:
                        print(f"content should not be empty")
                    if args.verbose:
                        print(f"-> {result_message['content']}")
                        
                    messages.append(result_message)
            else:
                final_response_message = message
                messages.append(message) 
                break
        else:
            print(f"Max iterations reached")
        if final_response_message:
            print(f"\nAgent Final Answer: {final_response_message.content}")
        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()