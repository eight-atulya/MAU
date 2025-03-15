# mau/utils/file_helpers.py

import os

def ensure_file_exists(file_path: str, default_content: str):
    """Create the file with default content if it does not exist."""
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(default_content)
        print(f"[INFO] Created default file: {file_path}")

def load_prompt(file_path: str) -> str:
    """Load and return the contents of a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
