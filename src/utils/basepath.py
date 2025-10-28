import os, sys
from pathlib import Path
BASE_PATH = ""
# Detect if running from bundled EXE
if getattr(sys, 'frozen', False):
    # When bundled, use the folder containing the EXE as the root
    BASE_PATH = Path(sys._MEIPASS)
else:
    # When running normally, use project root (parent of src)
    BASE_PATH = Path(__file__).resolve().parent.parent.parent

