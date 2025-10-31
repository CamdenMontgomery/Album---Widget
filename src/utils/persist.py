#This file is used for defining functions to help with dealing with persistent data
#there area  few things that will persist globally (stored in appdata) and then a few that will persist locally (stored in the workspace folder)
# Global
# - current workspace (so the user is brought back to it when they open the app)
# - current folder (so the user is brought back to it when they open the app)

#local
# - workspace pins (sinc each workspace will have its own pins)

#global ones will be stored in appdata/hermit/album as an ini file
#local ones will be store in the workspace folder as a settings.ini file


#global files will be read when the global state Store initialized
#local files will be read when the workspace changes
from PySide6.QtCore import QCoreApplication, QSettings
import os

def getGlobalConfigsRef():
    QCoreApplication.setOrganizationName("Hermit")
    QCoreApplication.setApplicationName("Album")   
    return QSettings()


#relies on global configs being up to date to return the proper information
def getLocalConfigsRef():

    global_config = getGlobalConfigsRef()
    workspace_path = global_config.value("workspace_dir")
    
    
    if workspace_path:
        path = os.path.join(workspace_path,"workspace.ini")
        local_config = QSettings(path, QSettings.IniFormat)
        return local_config
    
    return None

#build and return state object from global and local configs
def getStateFromConfigs():

    settings = getGlobalConfigsRef()   
    

    workspace_dir = settings.value("workspace_dir")
    contents = os.listdir(workspace_dir)
    workspace_folders = [name for name in contents if os.path.isdir(os.path.join(workspace_dir, name))]
    current_folder_name = settings.value("current_folder_name")
    hotkey_folders = getLocalConfigsRef().value("hotkey_folders") or {'1': '', '2': '', '3': '', '4': '', '5': ''}

    return {
        "workspace_dir": workspace_dir,
        "workspace_folders": workspace_folders,
        "current_folder_name": current_folder_name,
        "hotkey_folders": hotkey_folders,
        "show_widget": True
    }
    
