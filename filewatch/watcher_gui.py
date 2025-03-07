import tkinter as tk
from typing import Callable
from .file_change_frame import WatcherFrame
from .query_frame import QueryWindow


class WatcherGUI(tk.Tk):

    def __init__(self):
        """_summary_

        _extended_summary_

        Args:
            controller (_type_, optional): _description_. Defaults to None.
        """
        super().__init__()

        self.title("File Watcher")
        self.geometry("1000x800")

        self.__file_watch_frame = WatcherFrame(self)
        self.__file_watch_frame.pack(padx=5, pady=5)

        # window for query search results
        self.__query_frame = QueryWindow(self)
        self.__query_frame.pack(padx=5, pady=5, ipadx=5, ipady=5)

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


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
