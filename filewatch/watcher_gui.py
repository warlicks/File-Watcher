import tkinter as tk
from tkinter import W, E, BooleanVar, StringVar, Toplevel, ttk, filedialog, messagebox, Menu
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


        self.menu_bar = MenuBar(
            self,
            start_monitoring=self.start_watching,
            stop_monitoring=self.stop_watching,
            write_to_db=self.write_to_db,
            save_report=self.save_report
        )
        self.config(menu=self.menu_bar)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
    
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
   
    def on_exit(self):
        """Handles exit program request by calling ExitWindow class"""
        exit_window = ExitWindow(self)
        self.wait_window(exit_window)




class MenuBar(tk.Menu):
    """Class for managing menu bar of our application.
    Inherits from tk.Menu and contains File and Help menus.
    """
    def __init__(self, parent, start_monitoring, stop_monitoring, write_to_db, save_report):
        super().__init__(parent)
        self.parent = parent

        self.start_monitoring = start_monitoring
        self.stop_monitoring = stop_monitoring
        self.write_to_db = write_to_db
        self.save_report = save_report

        self._create_menus()
        self._bind_shortcuts()

    def _create_menus(self):
        """Create and configure the menu bar"""
        self._create_file_menu()
        self._create_monitor_menu()
        self._create_help_menu()

    def _create_file_menu(self):
        """Creates file menu, also incorporates keyboard shortcuts."""

        file_menu = Menu(self, tearoff=0)
        file_menu.add_command(label="Save Report", accelerator="Ctrl+S", command=self.save_report)
        file_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.parent.quit)
        self.add_cascade(label="File", menu=file_menu)

    def _create_monitor_menu(self):
        monitor_menu = Menu(self, tearoff=0)
        monitor_menu.add_command(label="Start Monitoring", accelerator="Ctrl+M", command=self.start_monitoring)
        monitor_menu.add_command(label="Stop Monitoring", accelerator="Ctrl+X", command=self.stop_monitoring)
        monitor_menu.add_command(label="Write to Database", accelerator="Ctrl+D", command=self.write_to_db)
        self.add_cascade(label="Monitor", menu=monitor_menu)

    def _create_help_menu(self):
        help_menu = Menu(self, tearoff=0)
        help_menu.add_command(label="About", accelerator="Ctrl+H", command=self.show_about)
        self.add_cascade(label="Help", menu=help_menu)

    def _bind_shortcuts(self):
        """Bind shortcuts to actions."""

        self.parent.bind_all("<Control-s>", lambda e: self.save_report())
        self.parent.bind_all("<Control-q>", lambda e: self.parent.quit())
        self.parent.bind_all("<Control-m>", lambda e: self.start_monitoring())
        self.parent.bind_all("<Control-x>", lambda e: self.stop_monitoring())
        self.parent.bind_all("<Control-d>", lambda e: self.write_to_db())
        self.parent.bind_all("<Control-h>", lambda e: self.show_about())

    def show_about(self):
        """Displays an "About" program section"""
        messagebox.showinfo(
            "About",
            "FileWatcher Monitor v1.0\nDeveloped by Sean Warlick and Ainsley Yoshizumi\n"
                    "This program monitors file activity and writes all activity to a SQL database."
                    "Users can also send and generate reports"
        )

class ExitWindow(tk.Toplevel):
    """Class for exit window, requires confirmation from user that they want to quit program"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Confirm Exit")
        self.geometry("300x150")
        self.parent = parent

        tk.Label(self, text="Are you sure you wish to exit?").pack(pady=20)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        yes_button = tk.Button(button_frame, text="Yes", command=self.confirm_exit)
        yes_button.pack(side=tk.LEFT, padx=5)

        no_button = tk.Button(button_frame, text="No", command=self.cancel_exit)
        no_button.pack(side=tk.RIGHT, padx=5)

    def confirm_exit(self):
        self.parent.destroy()
        self.destroy()

    def cancel_exit(self):
        self.destroy()


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
