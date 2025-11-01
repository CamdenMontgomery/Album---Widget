import sys
from pathlib import Path

def get_base_path() -> Path:
    """
    Determines the base path of the application depending on whether it's 
    running from a bundled executable or the source code.

    When the application is bundled (e.g., using PyInstaller), it uses 
    the folder containing the executable. Otherwise, it assumes the script
    is being run from the project source directory.

    Returns:
        Path: The base path for the application, which will be the folder
              containing the executable when bundled, or the project root
              in development.
    """
    if getattr(sys, 'frozen', False):
        # When running from a bundled EXE, the base path is where the EXE is located
        return Path(sys._MEIPASS)
    else:
        # When running normally, the base path is the root of the project
        return Path(__file__).resolve().parent.parent.parent

# Set BASE_PATH globally
BASE_PATH = get_base_path()
