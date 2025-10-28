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


def getGlobalConfigsRef():
    QCoreApplication.setOrganizationName("Hermit")
    QCoreApplication.setApplicationName("Album")   

    return QSettings()

#Returns state object omitting locally dependent fields like hotkey_folders 
def getStateFromGlobalConfigs():
    QCoreApplication.setOrganizationName("Hermit")
    QCoreApplication.setApplicationName("Album")   
    
    settings = QSettings()    
    return {
        "workspace_dir": settings.value("workspace_dir"),
        "workspace_folders": settings.value("workspace_folders"),
        "current_folder_name": settings.value("current_folder_name"),
        "hotkey_folders": {'1': '', '2': '', '3': '', '4': '', '5': ''},
        "show_widget": True
    }
    
def setGlobalConfigsFromState(state):
    QCoreApplication.setOrganizationName("Hermit")
    QCoreApplication.setApplicationName("Album")   
    
    settings = QSettings()   
    settings.setValue("workspace_dir", state["workspace_dir"])
    settings.setValue("workspace_folders", state["workspace_folders"])
    settings.setValue("current_folder_name", state["current_folder_name"])