from pathlib import Path

def loadStylesheets(*paths):
    """
    Load stylesheets from the provided file paths and combine them into a single string.
    
    Args:
        *paths: File paths of individual stylesheets to be loaded.
        
    Returns:
        str: Combined stylesheet content.
    """
    combined = []
    for path in paths:
        file_path = Path(path)
        
        # Check if file exists and is readable
        if file_path.exists() and file_path.is_file():
            try:
                # Read and append the content of the file
                combined.append(file_path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"Error reading stylesheet {file_path}: {e}")
        else:
            print(f"Warning: {file_path} does not exist or is not a file.")
    
    return "\n".join(combined)


def loadStylesheetsFromFolder(path):
    """
    Load stylesheets recursively from a folder and combine them into a single string.
    
    Args:
        path: The folder path to search for .qss files.
        
    Returns:
        str: Combined stylesheet content from all .qss files in the folder.
    """
    base_path = Path(path)
    
    # Check if the folder exists
    if not base_path.exists() or not base_path.is_dir():
        print(f"Error: {base_path} is not a valid directory.")
        return ""
    
    qss_files = sorted(base_path.rglob("*.qss"))  # Recursively find all .qss files
    
    combined = []
    for qss_file in qss_files:
        try:
            # Read the .qss file content and append to the combined list
            combined.append(qss_file.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Error reading stylesheet {qss_file}: {e}")
    
    return "\n".join(combined)
