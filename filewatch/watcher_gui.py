import tkinter as tk
from typing import Callable
from .file_change_frame import WatcherFrame
from .query_frame import ActionButton, QueryWindow


class WatcherGUI(tk.Tk):

    def __init__(self):
        """Creates the GUI for the user to use the FileWatcher Program

        The WatcherGUI takes the GUI objects for managing the file monitoring and querying
        the database and combines them to create the overall interface.

        The class also manages the safe exposure of attributes (variables, widgets and methods)
        needed by the ViewManager. These are all exposed via properties.
        """
        super().__init__()

        self.title("File Watcher")
        self.geometry("1000x800")

        self.__file_watch_frame = WatcherFrame(self)
        self.__file_watch_frame.pack(padx=5, pady=5)

        # window for query search results
        self.__query_frame = QueryWindow(self)
        self.__query_frame.pack(padx=5, pady=5, ipadx=5, ipady=5)

    # Define properties for things we need to pass to the Controller. This lets us keep
    # the logic out of the GUI code.
    @property
    def status_label(self):
        """Returns File Watcher Status Label"""
        return self.__file_watch_frame.status_label

    @property
    def status_label_text(self) -> tk.StringVar:
        """Returns Status Label Text Variable"""
        return self.__file_watch_frame.status_label_text

    @property
    def start_button(self) -> ActionButton:
        """Returns the Start Button Widget"""
        return self.__file_watch_frame.start_button

    @property
    def stop_button(self) -> ActionButton:
        """Returns the Stop Button Widget"""
        return self.__file_watch_frame.stop_button

    @property
    def dir_to_watch(self) -> str:
        """Returns the directory selected for monitoring"""
        return self.__file_watch_frame.selected_directory.get()

    @property
    def file_ext_to_watch(self) -> str:
        """Returns the file extensions selected for monitoring"""
        return self.__file_watch_frame.file_ext_to_watch

    @property
    def recursive(self) -> bool:
        """Returns the boolean indicating if sub-directories should be monitored"""
        return self.__file_watch_frame.recursive

    @property
    def search_button(self) -> ActionButton:
        """Returns the Button Widget for Starting the Search"""
        return self.__query_frame.query_frame.search_button

    @property
    def query_choice(self) -> tk.StringVar:
        """Returns the string variable indicating how the database will be searched."""
        return self.__query_frame.query_frame.query_choice

    @property
    def file_extension(self) -> tk.StringVar:
        """Returns the file extension for the database search"""
        return self.__query_frame.query_frame.query_string

    @property
    def query_action_type(self) -> tk.StringVar:
        """Returns the file action type selected when querying by action type"""
        return self.__query_frame.query_frame.query_action_type

    @property
    def query_directory_string(self) -> tk.StringVar:
        """Returns the string var with the directory when querying by directory"""
        return self.__query_frame.query_frame.query_directory_string

    @property
    def start_time_string(self) -> tk.StringVar:
        """Returns the start timestamp when querying by time period"""
        return self.__query_frame.query_frame.start_time_string

    @property
    def end_time_string(self) -> tk.StringVar:
        """Returns the end timestamp when querying by time period"""
        return self.__query_frame.query_frame.end_time_string

    @property
    def insert_query_result(self) -> Callable:
        """Returns the method for inserting data into the query result frame."""
        return self.__query_frame.query_result_frame.insert_row

    @property
    def email_sender(self) -> tk.StringVar:
        """Returns the string variable with the email senders email address"""
        return self.__query_frame.query_frame.email_sender

    @property
    def email_password(self) -> tk.StringVar:
        """Returns the password for the senders email account when sending a report."""
        return self.__query_frame.query_frame.email_password

    @property
    def email_recipients(self) -> tk.StringVar:
        """Returns the email address of the report recipient"""
        return self.__query_frame.query_frame.email_recipients

    @property
    def report_file_name(self) -> tk.StringVar:
        """Returns the full file name for the file activity report"""
        return self.__query_frame.query_frame.report_file_name

    @property
    def keep_report(self) -> tk.BooleanVar:
        """Returns the boolean indicating if the report should be kept after being emailed."""
        return self.__query_frame.query_frame.keep_report

    @property
    def send_report_cmd(self):
        """Returns the send report command variable"""
        return self.__query_frame.query_frame.send_report_cmd

    @send_report_cmd.setter
    def send_report_cmd(self, value: Callable):
        """Sets the send report command"""
        self.__query_frame.query_frame.send_report_cmd = value


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
