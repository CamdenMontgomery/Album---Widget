from pathlib import Path

def loadStylesheets(*paths):
    combined = ""
    for path in paths:
        file_path = Path(path)
        if file_path.exists():
            combined += file_path.read_text() + "\n"
    return combined

def loadStylesheetsFromFolder(path):
    base_path = Path(path)
    qss_files = sorted(base_path.rglob("*.qss"))  # recursive search
    
    combined = ""
    for qss_file in qss_files:
        combined += qss_file.read_text(encoding="utf-8") + "\n"
        
    return combined

