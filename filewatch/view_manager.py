import csv
import datetime as dt
import os

from .email_client import ReportEmail as email
from .file_database import FileWatcherDatabase
from .watcher import FileWatcher
from .watcher_gui import WatcherGUI
from .file_watch import FileHandler

from fileinput import filename


class ViewManager:
    def __init__(self, model: FileHandler, view: WatcherGUI):
        """The ViewManager manages interactions between the GUI and the FileHandler

        The ViewManager is the controller layer between the FileHandler and the GUI. It
        takes us er inputs from the GUI and uses them to call the appropriate FileHandler
        or FileWatcherDatabase methods.

        Args:
            model (FileHandler): FileHandler used to monitor for file changes.
            view (WatcherGUI): The GUI object being used by the user.
        """
        self.__handler = model
        self.__view = view
        self.__handler.register_observers(self)

        # Set up the database connection.
        self.__db = FileWatcherDatabase()
        self.__db.create_database_connection()
        self.__db.create_table()

        # the configure method lets us set the action via the controller layer after
        # defining the button in the viewer layer.
        self.__view.start_button.configure(command=self.send_start_watching)
        self.__view.stop_button.configure(command=self.send_stop_watching)
        self.__view.search_button.configure(command=self.start_database_search)

        self.__view.send_report_cmd = self.generate_report

    def send_start_watching(self):
        """Manages starting the file watcher.

        The method manages the interactions between the GUI and the watcher. The method
        gets attached to the GUI's start button. When the button is pressed it calls
        the watcher's start_watching method.
        """
        print("send_start_watching() called")  # for debugging, remove later
        print(f"Watching {self.__view.dir_to_watch}")
        self.__watcher = FileWatcher(self.__handler)

        # TK doesn't have a file a list variable, so we need to convert the string to
        # a list.
        if self.__view.file_ext_to_watch is None:
            ext = []
        else:
            ext = self.__view.file_ext_to_watch.split(",")

        self.__watcher.start_watching(
            self.__view.dir_to_watch, self.__view.recursive, ext
        )
        self.__view.status_label_text.set(f"Watching {self.__view.dir_to_watch}")
        self.__view.status_label.configure(foreground="green")  # ✅ UI Update

    def send_stop_watching(self):
        """Passes press of the Stop Watching button to the file watcher.

        The method manages the interactions between the GUI and the watcher. The method
        gets attached to the GUI's stop button. When the button is pressed it calls
        the watcher's stop_watching method.
        """
        print("send_stop_watching() called")  # for debug, remove later
        print(f"Stopped Watching {self.__view.dir_to_watch}")
        self.__watcher.stop_watching()
        self.__view.status_label_text.set("Status: Stopped")
        self.__view.status_label.configure(foreground="red")  # ✅ UI Update

    def start_database_search(self):
        """Manages Database Searches from the GUI

        The method takes user inputs from the GUI and passes them as parameters to
        the appropriate database query. When the query results are returned, they are
        passed to the GUI so they can be displayed to the user.
        """
        query_type = self.__view.query_choice.get()

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

        self.__current_results = result
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

        # human readable format
        timestamp_human = datetime.datetime.fromtimestamp(timestamp_int).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_message = (
            f"{timestamp_human} - {event_type.upper()} - {filename} in {directory}"
        )
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

    def generate_report(self):
        """Manages the generation of file activity report

        When a user selects the options to generate a report it takes the inputs from the
        GUI to write the results to a file and then send them via email.
        """
        subject = "File Activity Report"
        body = "The requested file activity report is attached."
        report_location = self._write_report(
            self.__current_results, self.__view.report_file_name.get()
        )
        email.email_report(
            self.__view.email_sender.get(),
            self.__view.email_password.get(),
            self.__view.email_recipients.get(),
            subject,
            body,
            attachment=report_location,
        )

        if not self.__view.keep_report.get():
            os.remove(self.__view.report_file_name.get())

    def _write_report(
        self, results: list, result_file: str = "./file_activity_report.csv"
    ) -> str:
        """Internal method for writing file activity report to directory.

        Saves the report to a CSV file.

        Args:
            results (list): The results of an activity query
            result_file (str, optional): The directory where the file will be saved.
              Defaults to "./file_activity_report.csv".

        Returns:
            str: The name of the report file.
        """
        header = ["File", "Action", "Time", "File Type", "Move Destination"]
        report_name = result_file
        with open(report_name, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(results)

        return report_name
