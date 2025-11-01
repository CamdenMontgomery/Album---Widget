from pynput import keyboard
from PySide6.QtCore import QObject, Signal
from enums.EActionTypes import EActionTypes
from utils.UseStore import UseStore

class HotKeyManager(QObject, UseStore):
    """
    This class manages global hotkeys and triggers corresponding actions
    via signals to communicate with the main Qt application thread.
    """
    
    # Signal to safely communicate between pynput's thread and the Qt thread
    _cross_thread = Signal(int, str)

    def __init__(self):
        """
        Initialize the HotKeyManager, bind hotkeys, and start listening for them.
        """
        super().__init__()
        
        # Define Hotkeys and their corresponding actions
        self.hotkeys = keyboard.GlobalHotKeys(self._get_hotkey_bindings())

        # Connect the signal to the Qt thread method for handling actions
        self._cross_thread.connect(self.qtThread)

        # Start listening for hotkeys
        self.hotkeys.start()

    def _get_hotkey_bindings(self):
        """
        Return a dictionary of hotkeys and their corresponding actions.
        
        Hotkeys are defined with an action type that is triggered when the hotkey is pressed.
        This allows easy maintenance of hotkeys and their mappings.
        """
        return {
            # Folder Switching (Alt + [1-5])
            '<alt>+1': lambda: self._trigger_action(EActionTypes.FOLDER_HOTKEY, '1'),
            '<alt>+2': lambda: self._trigger_action(EActionTypes.FOLDER_HOTKEY, '2'),
            '<alt>+3': lambda: self._trigger_action(EActionTypes.FOLDER_HOTKEY, '3'),
            '<alt>+4': lambda: self._trigger_action(EActionTypes.FOLDER_HOTKEY, '4'),
            '<alt>+5': lambda: self._trigger_action(EActionTypes.FOLDER_HOTKEY, '5'),

            # Tool Hotkeys (Alt + [z, x, c])
            '<alt>+z': lambda: self._trigger_action(EActionTypes.TOOL_HOTKEY, 'z'),
            '<alt>+x': lambda: self._trigger_action(EActionTypes.TOOL_HOTKEY, 'x'),
            '<alt>+c': lambda: self._trigger_action(EActionTypes.TOOL_HOTKEY, 'c'),
        }

    def _trigger_action(self, action_type, key):
        """
        Emit a signal to trigger an action on the main Qt thread.

        Args:
            action_type (int): The action type constant (e.g., EActionTypes.FOLDER_HOTKEY).
            key (str): The key pressed that triggers the action.
        """
        self._cross_thread.emit(action_type, key)

    def qtThread(self, action_type, key):
        """
        Slot to handle the action on the Qt main thread using the dispatched signal.
        
        Args:
            action_type (int): The action type constant.
            key (str): The key associated with the hotkey that was pressed.
        """
        self.store_.dispatch(action_type, key)

    def on_state_changed(self):
        """
        Handle state changes if needed. This can be expanded if state changes need to trigger specific behavior.
        """
        pass
