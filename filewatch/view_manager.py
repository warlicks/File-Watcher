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
        self.__view.search_function = self.start_database_search

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
        query_value = self.__view.query_string.get()

        if query_type == "File Type":
            result =  self.search_by_extension(query_value)
        elif query_type == "File Action":
            result = self.search_by_action(query_value)
        elif query_type == "File Directory":
            result = self.search_by_directory(query_value)
        else:
            result = "Invalid Query Type"

        #For UI
        self.__view.query_result.set(result)
        print(f"Search Query: {query_type} -> {query_value} | Result: {result}")
        # print(
        #     f"Started Database Query by {self.__view.query_choice.get()}, {self.__view.query_string.get()}"
        # )
        # self.__view.query_result.set("Fake Result")

    def execute_query(self, query: str, params: tuple) -> str:
        """Helper method that runs DB queries and returns results as a formatted string"""
        try:
            conn = sqlite3.connect("file_watcher.db")  ##stilll have to find actual path
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            conn.close()

            if not results:
                return "No results found."

            #return "\n".join([", ".join(map(str, row)) for row in results])

        except sqlite3.Error as e:
            return f"Database error: {str(e)}"


    def search_by_extension(self, extension: str) -> str:
        """Search for files with a given extension."""
        query = "SELECT filename,  directory, action, timestamp FROM file_event WHERE filename LIKE ?"
        params = (f'%.{extension}',)
        return self.execute_query(query, params)

    def search_by_action(self, action: str) -> str:
        """Search for files by action (created, modified, etc.)."""
        query = "SELECT filename, directory, timestamp FROM file_events WHERE action = ?"
        params = (action,)
        return self.execute_query(query, params)

    def search_by_directory(self, directory: str) -> str:
        """Search for files in a specified directory."""
        query = "SELECTfilename, action, timestamp FROM file_events WHERE directory = ?"
        params = (directory,)
        return self.execute_query(query, params)

    def notify(self):

        # Needs to pass the events to the GUI's log window.
        # Needs to insert the data into the database.
        pass
