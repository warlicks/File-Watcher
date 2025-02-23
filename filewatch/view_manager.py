from .watcher import FileWatcher
from .watcher_gui import WatcherGUI


class ViewManager:
    def __init__(self, model: FileWatcher, view: WatcherGUI):
        self.__watcher = model
        self.__view = view
        self.__watcher.handler.register_observers(self)
        # self.__database_tools = FileWatcherDatabase()

        # the configure method lets us set the action via the controller layer after
        # defining the button in the viewer layer.
        self.__view.start_button.configure(command=self.send_start_watching)
        self.__view.stop_button.configure(command=self.send_stop_watching)

    def send_start_watching(self):
        """Manages starting the file watcher.

        The method manages the interactions between the GUI and the watcher. The method
        gets attached to the GUI's start button. When the button is pressed it calls
        the watcher's start_watching method.
        """
        print(f"Watching {self.__view.dir_to_watch}")
        self.__watcher.start_watching(
            self.__view.dir_to_watch,
            # self.__view.recursive_watch,
            # self.__view.file_extensions,
        )

    def send_stop_watching(self):
        """Passes press of the Stop Watchihng button to the file watcher. .

        The method manages the interactions between the GUI and the watcher. The method
        gets attached to the GUI's stop button. When the button is pressed it calls
        the watcher's stop_watching method.
        """
        print(f"Stopped Watching {self.__view.dir_to_watch}")
        self.__watcher.stop_watching()

    def notify(self):

        # Needs to pass the events to the GUI's log window.
        # Needs to insert the data into the database.
        pass
