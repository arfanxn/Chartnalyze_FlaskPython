import os
from flask import current_app
from werkzeug.datastructures import FileStorage

def get_file_size (file: (FileStorage | None)): 
    if file == None: 
        return None
    pos = file.stream.tell()
    file.stream.seek(0, 2)  # pindah ke akhir file
    file_size = file.stream.tell()  # posisi pointer di akhir = ukuran file
    file.stream.seek(pos)  # kembalikan posisi pointer ke awal
    return file_size

def get_app_root_path() -> str:
    """Return the absolute path to the Flask app root directory."""
    return current_app.root_path

def get_parent_directory(path: str) -> str:
    """Return the parent directory of the given path."""
    return os.path.dirname(path)

def join_path(*paths: str) -> str:
    """Join multiple path components into a single path."""
    return os.path.join(*paths)

def get_public_folder_path() -> str:
    """Return the absolute path to the 'public' folder located alongside the Flask app folder."""
    app_root = get_app_root_path()
    parent_dir = get_parent_directory(app_root)
    public_path = join_path(parent_dir, 'public')
    return public_path
