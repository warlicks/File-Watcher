from .watcher import FileWatcher
from .file_database import FileWatcherDatabase
from .watcher_gui import WatcherGUI
import datetime as dt

from fileinput import filename


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
        print("send_start_watching() called") #for debugging, remove later
        print(f"Watching {self.__view.dir_to_watch}")
        self.__watcher.start_watching(self.__view.dir_to_watch)
        self.__view.update_status("Status: Watching", "green")  # ✅ UI Update


    def send_stop_watching(self):
        """Passes press of the Stop Watching button to the file watcher. .

        The method manages the interactions between the GUI and the watcher. The method
        gets attached to the GUI's stop button. When the button is pressed it calls
        the watcher's stop_watching method.
        """
        print("send_stop_watching() called") #for debug, remove later
        print(f"Stopped Watching {self.__view.dir_to_watch}")
        self.__watcher.stop_watching()
        self.__view.update_status("Status: Stopped", "red")  # ✅ UI Update


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
        """Handles notifications from the FileWatcher by updating GUI log panel w event
        and inserts event into DB

        Args:
            event_type (str): Type of event (created, modified, etc.)
            filename (str): Name of edited file
            directory (str): Directory where event occurred
            timestamp (float): Timestamp of when event occured

            """
        timestamp_int = int(timestamp)

        #human readable format
        timestamp_human = datetime.datetime.fromtimestamp(timestamp_int).strftime('%Y-%m-%d %H:%M:%S')

        log_message = f"{timestamp_human} - {event_type.upper()} - {filename} in {directory}"
        self.__view.update_log(log_message)

        try:
            conn = sqlite3.connect("file_watcher.db")
            cursor = conn.cursor()
            query = """INSERT INTO file_events (filename, directory, action, timestamp 
                    VALUES (?, ?, ?, ?)"""
            cursor.execute(query, (filename, directory, event_type, timestamp_int))
            conn.commit()
            conn.close()

        except sqlite3.Error as e:
            error_message = f"Database error: {str(e)}"
            self.__view.update_log(error_message)
            print(error_message)