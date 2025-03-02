from .watcher import FileWatcher
from .file_database import FileWatcherDatabase
from .watcher_gui import WatcherGUI
import datetime as dt


class ViewManager:
    def __init__(self, model: FileWatcher, view: WatcherGUI):
        self.__watcher = model
        self.__view = view
        self.__watcher.handler.register_observers(self)

        # Set up the database connection.
        self.__db = FileWatcherDatabase()
        self.__db.create_database_connection()
        self.__db.create_table()

        # the configure method lets us set the action via the controller layer after
        # defining the button in the viewer layer.
        self.__view.start_button.configure(command=self.send_start_watching)
        self.__view.stop_button.configure(command=self.send_stop_watching)
        self.__view.search_button.configure(command=self.start_database_search)

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

    def start_database_search(self):
        """Handles DB search requests"""
        query_type = self.__view.query_choice.get()
        query_value = self.__view.file_extension.get()

        if query_type == "File Type":
            print("Searching by file type")
            result = self.__db.query_by_file_extension(self.__view.file_extension.get())
        elif query_type == "File Action":
            print("Search By File Action")
            result = self.__db.query_by_event_type(
                self.__view.query_action_type.get().lower()
            )
        elif query_type == "File Directory":
            print("Search By File Directory")
            result = self.__db.query_by_event_location(
                self.__view.query_directory_string.get()
            )
        elif query_type == "Action Time":
            ts_format = "%Y-%m-%d %H:%M:%S"
            start_time_epoch = dt.datetime.strptime(
                self.__view.start_time_string.get(), ts_format
            ).timestamp()
            end_time_epoch = dt.datetime.strptime(
                self.__view.end_time_string.get(), ts_format
            ).timestamp()
            result = self.__db.query_by_event_date(start_time_epoch, end_time_epoch)

        for row in result:
            self.__view.insert_query_result(
                (row[0], row[1], dt.datetime.fromtimestamp(row[2]), row[3], row[4])
            )

    def notify(self):

        # Needs to pass the events to the GUI's log window.
        # Needs to insert the data into the database.
        pass
