import tkinter as tk
from tkinter import W, E, BooleanVar, StringVar, Toplevel, ttk, filedialog
from typing import Callable
from file_change_frame import WatcherFrame
from query_frame import QueryWindow, ActionButton


class WatcherGUI(tk.Tk):

    def __init__(self):
        """_summary_

        _extended_summary_

        Args:
            controller (_type_, optional): _description_. Defaults to None.
        """
        super().__init__()

        self.title("File Watcher")

        self.geometry("800x600")

        self.__file_watch_frame = WatcherFrame(self)
        self.__file_watch_frame.pack()

        # window for query search results
        self.__query_frame = QueryWindow(self)
        self.__query_frame.pack(
            pady=5,
        )  # anchor=E, side=tk.RIGHT)

    # Define properties for things we need to pass to the Controller.
    @property
    def status_label(self):
        return self.__file_watch_frame.status_label

    @property
    def status_label_text(self):
        return self.__file_watch_frame.status_label_text

    @property
    def start_button(self):
        return self.__file_watch_frame.start_button

    @property
    def stop_button(self):
        return self.__file_watch_frame.stop_button

    @property
    def dir_to_watch(self) -> str:
        return self.__file_watch_frame.selected_directory.get()

    @property
    def search_button(self):
        return self.__query_frame.query_frame.search_button

    @property
    def query_choice(self):
        return self.__query_frame.query_frame.query_choice

    @property
    def file_extension(self):
        return self.__query_frame.query_frame.query_string

    @property
    def query_action_type(self):
        return self.__query_frame.query_frame.query_action_type

    @property
    def query_directory_string(self):
        return self.__query_frame.query_frame.query_directory_string

    @property
    def start_time_string(self):
        return self.__query_frame.query_frame.start_time_string

    @property
    def end_time_string(self):
        return self.__query_frame.query_frame.end_time_string

    @property
    def insert_query_result(self):
        return self.__query_frame.query_result_frame.insert_row

    @property
    def email_sender(self):
        return self.__query_frame.query_frame.email_sender

    @property
    def email_password(self):
        return self.__query_frame.query_frame.email_password

    @property
    def email_recipients(self):
        return self.__query_frame.query_frame.email_recipients

    @property
    def report_file_name(self):
        return self.__query_frame.query_frame.report_file_name

    @property
    def keep_report(self):
        return self.__query_frame.query_frame.keep_report

    @property
    def send_report_cmd(self):
        return self.__query_frame.query_frame.send_report_cmd

    @send_report_cmd.setter
    def send_report_cmd(self, value: Callable):
        self.__query_frame.query_frame.send_report_cmd = value


class ActionFrame(ttk.Frame):
    """Class For Managing Frame with buttons to start and stop watching a directory.
    Inherits from ttk.Frame
    """

    def __init__(self, parent):
        """Initializes the ActionFrame with buttons to start and stop watching a directory.


        Args:
            parent: Parent Tkinter object
        """

        # def __init__(self, parent, start_callback, stop_callback):

        super().__init__(parent)
        self.start_button = ActionButton(self, "Start Watching")
        self.start_button.pack(side=tk.LEFT, padx=5)
        #         self.start_button.configure(command=start_callback)

        self.stop_button = ActionButton(self, "Stop Watching")
        self.stop_button.pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
