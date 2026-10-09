import os
from pathlib import Path
from utils import resolve_inside


def create_folder(working_directory: str, folder_name: str, directory: str):
    try:
        target_directory = resolve_inside(working_directory, directory)
        
        if not os.path.isdir(target_directory):
            raise FileNotFoundError(f"Specified `{directory}` is not a directory")

        new_folder_name = resolve_inside(target_directory, folder_name)        
        target_path = Path(new_folder_name)
        
        if target_path.exists():
            raise FileExistsError(f"Path `{folder_name}` already exists")
        
        target_path.mkdir(parents=True, exist_ok=False)
               
        return f"Folder '{new_folder_name}' created successfully."
    except Exception as e:
        return str(e)        

