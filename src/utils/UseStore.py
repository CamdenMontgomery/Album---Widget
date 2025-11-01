from abc import  abstractmethod
from utils.Store import store
from PySide6.QtCore import QTimer


class UseStore:
    """Base class to connect to the application's store and listen for state changes.
    
    This class ensures that any subclass is able to react to state changes from
    the `store` and initialize properly when the Qt application starts. It uses
    a deferred call to `on_state_changed` to ensure that the subclass is
    properly initialized once Qt internals are ready.
    """

    def __init__(self):
        """
        Initialize the UseStore instance by connecting to the global store and 
        setting up the state change listener. The `on_state_changed` method will 
        be triggered when the state is updated.
        """
        # Store reference
        self.store_ = store
        
        # Connect state change signal to the subclass's implementation of on_state_changed
        store.state_changed.connect(self.on_state_changed)
        
        # Use a QTimer to defer the state change handling to after Qt internals are initialized
        QTimer.singleShot(0, self.on_state_changed)

    @abstractmethod
    def on_state_changed(self):
        """
        Abstract method to handle the state change. Must be implemented by subclasses.
        
        This method will be called whenever the state changes. Subclasses should
        implement their specific logic for handling state updates.

        Example:
            def on_state_changed(self):
                current_state = self.store_.state
                # Do something with the updated state
        """
        pass
