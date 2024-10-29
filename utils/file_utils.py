# utils/file_utils.py

import os

def list_image_files(directory):
    """
    List all image files in the given directory.

    Parameters:
    - directory (str): Path to the directory.

    Returns:
    - List[str]: List of image filenames.
    """
    supported_extensions = ('.jpg', '.jpeg', '.png')
    return [f for f in os.listdir(directory) if f.lower().endswith(supported_extensions)]
