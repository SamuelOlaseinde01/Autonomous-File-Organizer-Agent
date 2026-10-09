import os
from utils import resolve_inside


def get_files_info(working_directory: str, directory: str):
    try:        
        target_dir = resolve_inside(working_directory, directory)

        if not os.path.isdir(target_dir):
            raise FileNotFoundError(f"Specified `{directory}` is not a directory")
        
        contents = os.listdir(target_dir)
        files_info = "Results for the current directory: \n"
        for content in contents:
            content_path = os.path.join(target_dir, content)
            content_size = os.path.getsize(content_path)
            is_dir = os.path.isdir(content_path)
            files_info += f"- {content}: size={content_size}bytes, is_dir={is_dir}\n"
        return files_info
    except Exception as e:
        return str(e)
    