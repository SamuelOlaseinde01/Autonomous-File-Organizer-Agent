import json
from functions import get_files_info, create_folder, move_file
from collections.abc import Callable

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)"
                }
            },
        "required": ["directory"]
        },
    }
}

schema_create_folder = {
    "type": "function",
    "function": {
        "name": "create_folder",
        "description": "Create folder at relative subpath inside workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "folder_name": {
                    "type": "string",
                    "description": "The name of the new folder to create. Do not include path slashes."
                },
                "directory": {
                    "type": "string",
                    "description": "The relative sub-directory path inside the current workspace where this folder should live."
                }
            },
            "required": ["folder_name", "directory"]
        }
    }
}

schema_move_file = {
    "type": "function",
    "function": {        
        "name": "move_file",
        "description": "Moves a file from a source location to a destination folder inside a specified working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "source_file": {
                    "type": "string",
                    "description": "The relative path of the file to be moved (e.g., 'image/img1.jpg')."
                },
                "destination": {
                    "type": "string",
                    "description": "The relative path of the target folder where the file should be moved (e.g., '.')."
                } 
            },
            "required": ["source_file", "destination"],
        }
    }
}


available_tools = [schema_get_files_info, schema_create_folder, schema_move_file]

def call_function(tool_call, verbose: bool = False) -> dict:
    try:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments or "{}")
        function_id = tool_call.id 
        
        function_args["working_directory"] = "files"
        
        function_dict: dict[str, Callable[..., str]] = {
            "get_files_info": get_files_info.get_files_info,
            "create_folder": create_folder.create_folder,
            "move_file": move_file.move_file
        }
                
        if verbose:
            print(f" - Calling function: {function_name}({function_args})")
        else:
            print(f" - Calling function: {function_name}")
        
        if function_name not in function_dict:         
            return {
                "role": "tool",
                "tool_call_id": function_id,
                "content": f"Error: Unknown function call: {function_name}"
            }
            
        result = function_dict[function_name](**function_args)
        
        return {
            "role": "tool",
            "tool_call_id": function_id,
            "content": result
        }
    except Exception as e:
        return {
            "role": "tool",
            "tool_call_id": getattr(tool_call, "id", "unknown"),
            "content": f"Error: {e}"
        }