# This file defines functions to help with dealing with persistent data.
# There are a few things that will persist globally (stored in appdata) and then a few that will persist locally (stored in the workspace folder).

# Global
# - current workspace (so the user is brought back to it when they open the app)
# - current folder (so the user is brought back to it when they open the app)

# Local
# - workspace pins (since each workspace will have its own pins)

# Global configs will be stored in appdata/hermit/album as an INI file
# Local configs will be stored in the workspace folder as a settings.ini file

# Global files will be read when the global state Store is initialized
# Local files will be read when the workspace changes

from PySide6.QtCore import QCoreApplication, QSettings
import os

def getGlobalConfigsRef():
    """
    Retrieve and return the global configuration settings using QSettings.
    
    These settings are stored in the appdata directory (appdata/hermit/album) as an INI file.
    """
    QCoreApplication.setOrganizationName("Hermit")
    QCoreApplication.setApplicationName("Album")
    return QSettings()


def getLocalConfigsRef():
    """
    Retrieve and return the local configuration settings for the current workspace.
    
    The settings are stored in the workspace folder as a workspace.ini file.
    If the local config does not exist, the file will be created.
    """
    global_config = getGlobalConfigsRef()
    
    # Retrieve the workspace directory path from the global config
    workspace_path = global_config.value("workspace_dir")
    
    if not workspace_path:
        # If no workspace path is set, create a default path
        workspace_path = os.path.join(os.path.expanduser("~"), "Hermit", "Workspaces")
        global_config.setValue("workspace_dir", workspace_path)  # Save the workspace path in global settings
    
    # Create the path for the local workspace settings file
    local_config_path = os.path.join(workspace_path, "workspace.ini")
    
    if not os.path.exists(local_config_path):
        # If the settings file doesn't exist, create the necessary directories and file
        os.makedirs(workspace_path, exist_ok=True)
        local_config = QSettings(local_config_path, QSettings.IniFormat)
        
        # Initialize default values (this can be expanded with more defaults if needed)
        local_config.setValue("hotkey_folders", {'1': '', '2': '', '3': '', '4': '', '5': ''})
        return local_config
    
    # If the settings file already exists, just return the QSettings reference
    return QSettings(local_config_path, QSettings.IniFormat)


def getStateFromConfigs():
    """
    Build and return the state object by merging global and local configuration data.
    
    The state includes information such as the current workspace, current folder,
    and hotkey folder settings. It combines values from both global and local config files.
    """
    # Retrieve global settings
    settings = getGlobalConfigsRef()
    
    # Retrieve the workspace directory from global settings
    workspace_dir = settings.value("workspace_dir")
    
    if not workspace_dir:
        workspace_dir = os.path.join(os.path.expanduser("~"), "Hermit", "Workspaces")  # Default workspace path
        settings.setValue("workspace_dir", workspace_dir)  # Save the workspace path in global settings
    
    # Get the list of folders in the workspace directory
    try:
        contents = os.listdir(workspace_dir)
        workspace_folders = [name for name in contents if os.path.isdir(os.path.join(workspace_dir, name))]
    except FileNotFoundError:
        # In case the workspace directory doesn't exist, create it
        os.makedirs(workspace_dir, exist_ok=True)
        workspace_folders = []  # No folders available
    
    # Retrieve the current folder name from global settings
    current_folder_name = settings.value("current_folder_name")
    
    # Retrieve the hotkey folders from the local settings
    local_config = getLocalConfigsRef()
    hotkey_folders = local_config.value("hotkey_folders") or {'1': '', '2': '', '3': '', '4': '', '5': ''}
    
    # Return the combined state object
    return {
        "workspace_dir": workspace_dir,
        "workspace_folders": workspace_folders,
        "current_folder_name": current_folder_name,
        "hotkey_folders": hotkey_folders,
        "show_widget": True
    }
