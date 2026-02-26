import sys
import os
from pathlib import Path

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_records_path():
    if getattr(sys, 'frozen', False):
        if sys.platform == 'win32':
            base_path = Path.home() / "Documents" / "NumberGuessingGame"
        elif sys.platform == 'linux':
            base_path = Path.home() / ".local" / "share" / "NumberGuessingGame"
        else:
            base_path = Path.home() / ".NumberGuessingGame"
    else:
        base_path = Path(__file__).parent
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path / "records.txt"