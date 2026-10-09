import os

def resolve_inside(working_directory: str, relative_path: str) -> str:
    base = os.path.realpath(working_directory)
    target = os.path.realpath(os.path.join(base, relative_path))
    if os.path.commonpath([base, target]) != base:
        raise PermissionError(f"`{relative_path}` is outside the working directory")
    return target