import tkinter as tk
from tkinter import W, E, BooleanVar, StringVar, Toplevel, ttk, filedialog
from typing import Callable
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

        self.directory_selection_frame = DirectorySelection(self)
        self.directory_selection_frame.pack(
            pady=10,
        )  # side=tk.LEFT)
        self.__dir_to_watch = self.directory_selection_frame.selected_directory

        self.frame_controls = ActionFrame(self)
        self.frame_controls.pack(pady=5)

        self.__status_label = StatusLabel(self)
        self.__status_label.pack(pady=5)

        # window for file-watching logs
        self.log_frame = tk.Frame(self)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(self.log_frame, text="Log Panel:").pack(anchor=tk.W)
        self.log_text = tk.Text(self.log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # window for query search results
        self.__query_frame = QueryWindow(self)
        self.__query_frame.pack(
            pady=5,
        )  # anchor=E, side=tk.RIGHT)

    # Define properties for things we need to pass to the Controller.
    @property
    def status_label(self):
        return self.__status_label

    @property
    def status_label_text(self):
        return self.__status_label.status_variable

    @property
    def start_button(self):
        return self.frame_controls.start_button

    @property
    def stop_button(self):
        return self.frame_controls.stop_button

    @property
    def dir_to_watch(self) -> str:
        return self.__dir_to_watch.get()

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


class StatusLabel(ttk.Label):
    def __init__(self, parent):
        super().__init__(parent)

        self.__status_variable = StringVar()
        self.__status_variable.set("Status: Idle")
        self.configure(textvariable=self.__status_variable, foreground="blue")

    @property
    def status_variable(self):
        return self.__status_variable


class DirectorySelection(ttk.Frame):
    """Class For Managing ttk Frame that allow you to select a directory.

    Inherits from ttk.Frame

    Also capture the selected directory and manages access to the selected directory.
    """

    def __init__(self, parent):
        """Creates an instance of a DirectorySelectionFrame

        Args:
            parent: The parent object where the frame is being added.
        """
        super().__init__(parent)
        self.__selected_directory = tk.StringVar()

        ttk.Label(self, text="Directory:").pack(side=tk.LEFT)
        self.dir_entry = ttk.Entry(
            self, width=40, textvariable=self.__selected_directory
        )
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(self, text="Select Directory", command=self.select_directory).pack(
            side=tk.LEFT
        )

    @property
    def selected_directory(self):
        return self.__selected_directory

    def select_directory(self):
        directory = filedialog.askdirectory()
        self.__selected_directory.set(directory)


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
