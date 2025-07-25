import os
import hashlib

def generate_unique_id(data: str) -> str:
    """Generates a unique ID based on the input data."""
    return hashlib.md5(data.encode()).hexdigest()

def get_file_extension(filename: str) -> str:
    """Extracts the file extension from a given filename."""
    return os.path.splitext(filename)[1].lower()

def is_valid_file_type(filename: str, allowed_extensions: list) -> bool:
    """Checks if the file has an allowed extension."""
    return get_file_extension(filename) in allowed_extensions