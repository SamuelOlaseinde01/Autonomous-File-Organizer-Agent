import os, shutil
from utils import resolve_inside

def move_file(working_directory: str, source_file: str, destination: str):
    try:
        target_file_path = resolve_inside(working_directory, source_file)
        destination_path = resolve_inside(working_directory, destination)
        
        if not os.path.isdir(destination_path):
            raise FileNotFoundError(f"Specified `{destination_path}` folder does not exist")
        if not os.path.isfile(target_file_path):
            raise FileNotFoundError(f"Specified `{source_file}` does not exist")
        
        shutil.move(target_file_path, destination_path)
        return "File moved successfully"
    except Exception as e:
        return str(e)
