import tkinter as tk
from tkinter import W, E, BooleanVar, StringVar, Toplevel, ttk, filedialog, messagebox, Menu
from typing import Callable


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


        self.menu_bar = MenuBar(
            self,
            start_monitoring=self.start_watching,
            stop_monitoring=self.stop_watching,
            write_to_db=self.write_to_db,
            save_report=self.save_report
        )
        self.config(menu=self.menu_bar)


        self.directory_selection_frame = DirectorySelection(self)
        self.directory_selection_frame.pack(
            pady=10,
        )  # side=tk.LEFT)
        self.__dir_to_watch = self.directory_selection_frame.selected_directory

        self.frame_controls = ActionFrame(self)


#         self.frame_controls = ActionFrame(self, self.start_watching, self.stop_watching)
        self.frame_controls.pack(pady=5)

        self.status_label = tk.Label(self, text="Status: Idle", fg="blue")
        self.status_label.pack(pady=5)

        self.__start_button = self.frame_controls.start_button
        self.__stop_button = self.frame_controls.stop_button

        #window for file-watching logs
        self.log_frame = tk.Frame(self)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(self.log_frame, text="Log Panel:").pack(anchor=tk.W)
        self.log_text = tk.Text(self.log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        #window for query search results
        self.query_result_frame = tk.Frame(self)
        self.query_result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(self.query_result_frame, text="Search Result:").pack(anchor=tk.W)
        self.query_result_text = tk.Text(self.query_result_frame, height=10)
        self.query_result_text.pack(fill=tk.BOTH, expand=True)

        self.__query_frame = QueryWindow(self)
        self.__query_frame.pack(
            pady=5,
        )  # anchor=E, side=tk.RIGHT)

        #self.exit_program() = ExitWindow(self)

    # Define properties for things we need to pass to the Controller.
    @property
    def start_button(self):
        return self.frame_controls.start_button

    @property
    def stop_button(self):
        return self.frame_controls.end_button

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


    def start_watching(self):
        print("Status: Watching", "green")
        self.update_status("Watching files for changes...", "green")

    def stop_watching(self):
        print("Status: Stopped", "red")
        self.update_status("Stopped watching files...", "red")

    def update_status(self, message: str, color: str):
        """Updates status label with message and text color"""
        if hasattr(self, "status_label"): #chec if exists
            self.status_label.config(text=message, fg=color)
            self.update()
        else:
            print(f"Status update failed: {message} ({color})")

    def write_to_db(self):
        print("Writing to database...")

    def save_report(self):
        print("Saving report...")

    def on_exit(self):
        if self.destroy():
            self.protocol("WM_DELETE_WINDOW", self.exit_window)



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

    #def __init__(self, parent, start_callback, stop_callback):

        super().__init__(parent)
        self.start_button = ActionButton(self, "Start Watching")
        self.start_button.pack(side=tk.LEFT, padx=5)
#         self.start_button.configure(command=start_callback)

        self.stop_button = ActionButton(self, "Stop Watching")
        self.stop_button.pack(side=tk.LEFT, padx=5)
#         self.stop_button.configure(command=stop_callback)


class ActionButton(tk.Button):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)


class QueryWindow(ttk.Frame):
    """Class for managing the Query Window

    Manages the query frame which allows the user to make a query of the database and
    displays the results.
    """

    def __init__(
        self,
        parent,
    ):
        """Initializes an instance of the QueryWindow class
        Manages the query frame which allows the user to make a query of the database and
        displays the results.

        Args:
            parent: parent Tkinter object.
        """
        super().__init__(parent)

        self.__query_frame = QueryFrame(self)
        self.__query_frame.pack()

        # Define Frame for Query Results
        ttk.Label(self, text="Query Results").pack(anchor=W, padx=5, pady=5)

        self.__query_result_frame = QueryResultFrame(
            self, columns=["File", "Action", "Time", "File Type", "Move Destination"]
        )
        self.__query_result_frame.pack(fill=tk.BOTH, expand=True)

    @property
    def query_frame(self):
        return self.__query_frame

    @property
    def query_result_frame(self):
        return self.__query_result_frame


class QueryFrame(ttk.Frame):
    """Class for managing frame for query options.

    Inherits from ttk.Frame
    """

    def __init__(
        self,
        parent,
    ):
        """Initializes an instance of the QueryFrame class.

        Manages the frame and widgets that allow the user to select how they want to
        query the database and the specify the query criteria based on that choice.

        Args:
            parent: The parent Tkinter object.
        """
        super().__init__(parent, padding=(10, 10, 10, 10))

        menu_vals = [
            "File Type",
            "File Action",
            "File Directory",
            "Action Time",
        ]
        # Define the variables for the query options & choices.
        self.__query_choice = StringVar()
        self.__query_string = StringVar()
        self.__query_action_type = StringVar()
        self.__query_directory_sting = StringVar()
        self.__start_time_string = StringVar()
        self.__end_time_string = StringVar()

        # Define Variables to Pass to the Report Generation Window
        self.__email_account = StringVar()
        self.__email_password = StringVar()
        self.__email_recipients = StringVar()
        self.__report_file_name = StringVar()
        self.__keep_report = BooleanVar()
        self.__send_report_cmd = None

        ## Select the overall query approach.
        self.__label_query_option = ttk.Label(self, text="Select Query Option:")
        self.__label_query_option.grid(row=0, column=1, sticky=W)
        self.__menu_wigit = ttk.OptionMenu(
            self,
            self.__query_choice,
            "File Type",
            *menu_vals,
            command=lambda x: self.activate_query_optons(),
        )
        self.__menu_wigit.grid(row=0, column=2, sticky=(W, E))

        # Search Options for file type
        self.__file_type_label = ttk.Label(self, text="Enter File Type:")
        self.__file_type_label.grid(row=1, column=0, sticky=W, padx=1, pady=5)
        self.__file_type_entry = ttk.Entry(self, textvariable=self.__query_string)
        self.__file_type_entry.grid(row=1, column=1, pady=5, sticky=(W, E))

        # search options for file action.
        self.__action_menu_lable = ttk.Label(self, text="Select Action:")
        self.__action_menu_lable.grid(row=1, column=2, pady=5, sticky=(W, E))
        self.__action_menu = tk.OptionMenu(
            self,
            self.__query_action_type,
            "Created",
            "Moved",
            "Deleted",
            "Modified",
        )
        self.__action_menu.grid(row=1, column=3, sticky=(W, E))
        self.__action_menu.config(state="disabled")

        # Search options for file directory.
        self.__file_directory_label = ttk.Label(self, text="Enter Directory:")
        self.__file_directory_label.grid(row=2, column=0, sticky=W, padx=1, pady=5)
        self.__file_directory_label.config(state="disabled")
        self.__file_directory_entry = ttk.Entry(
            self, textvariable=self.__query_directory_sting
        )
        self.__file_directory_entry.grid(row=2, column=1, pady=5, sticky=(W, E))
        self.__file_directory_entry.config(state="disabled")

        # Search Options for action time.
        self.__start_time_entry_lable = ttk.Label(self, text="Enter Start Time:")
        self.__start_time_entry_lable.grid(row=2, column=2, sticky=W, padx=1, pady=5)
        self.__start_time_entry_lable.config(state="disabled")
        self.__start_time_entry = ttk.Entry(self, textvariable=self.__start_time_string)
        self.__start_time_entry.grid(row=2, column=3, pady=5, sticky=(W, E))
        self.__start_time_entry.config(state="disabled")

        self.__end_time_entry_label = ttk.Label(self, text="& End Time:")
        self.__end_time_entry_label.grid(row=2, column=4, sticky=W, padx=1, pady=5)
        self.__end_time_entry_label.config(state="disabled")
        self.__end_time_entry = ttk.Entry(self, textvariable=self.__end_time_string)
        self.__end_time_entry.grid(row=2, column=5, pady=5, sticky=(W, E))
        self.__end_time_entry.config(state="disabled")

        self.__search_button = ActionButton(self, "Start Search")
        self.__search_button.grid(row=4, column=2, pady=5, sticky=(W, E))
        self.__generate_report_button = ActionButton(self, "Generate Report")
        self.__generate_report_button.config(
            command=lambda: self.spawn_report_generation()
        )
        self.__generate_report_button.grid(row=4, column=3, pady=5, sticky=(W, E))

    @property
    def menu_button(self):
        return self.__menu_button

    @property
    def is_open(self):
        return self._is_open

    @property
    def search_button(self):
        return self.__search_button

    @property
    def query_choice(self):
        return self.__query_choice

    @property
    def query_string(self):
        return self.__query_string

    @property
    def query_action_type(self):
        return self.__query_action_type

    @property
    def query_directory_string(self):
        return self.__query_directory_sting

    @property
    def start_time_string(self):
        return self.__start_time_string

    @property
    def end_time_string(self):
        return self.__end_time_string

    @property
    def email_sender(self):
        return self.__email_account

    @property
    def email_password(self):
        return self.__email_password

    @property
    def email_recipients(self):
        return self.__email_recipients

    @property
    def report_file_name(self):
        return self.__report_file_name

    @property
    def keep_report(self):
        return self.__keep_report

    @property
    def send_report_cmd(self):
        return self.__send_report_cmd

    @send_report_cmd.setter
    def send_report_cmd(self, value: Callable):
        self.__send_report_cmd = value

    def activate_query_optons(self):
        """Manages the state of the query options based on the selected query type.
        Only the entry choices that are relevant to the selected query approach are enabled.
        """

        if self.__query_choice.get() == "File Type":
            self.__action_menu_lable.config(state="disabled")
            self.__action_menu.config(state="disabled")
            self.__file_type_label.config(state="normal")
            self.__file_type_entry.config(state="normal")
            self.__file_directory_label.config(state="disabled")
            self.__file_directory_entry.config(state="disabled")

            self.__start_time_entry_lable.config(state="disabled")
            self.__start_time_entry.config(state="disabled")
            self.__end_time_entry_label.config(state="disabled")
            self.__end_time_entry.config(state="disabled")
        elif self.__query_choice.get() == "File Action":
            self.__action_menu_lable.config(state="normal")
            self.__action_menu.config(state="normal")
            self.__file_type_label.config(state="disabled")
            self.__file_type_entry.config(state="disabled")
            self.__file_directory_label.config(state="disabled")
            self.__file_directory_entry.config(state="disabled")
            self.__start_time_entry_lable.config(state="disabled")
            self.__start_time_entry.config(state="disabled")
            self.__end_time_entry_label.config(state="disabled")
            self.__end_time_entry.config(state="disabled")
        elif self.__query_choice.get() == "File Directory":
            self.__action_menu_lable.config(state="disabled")
            self.__action_menu.config(state="disabled")
            self.__file_type_label.config(state="disabled")
            self.__file_type_entry.config(state="disabled")
            self.__file_directory_label.config(state="enabled")
            self.__file_directory_entry.config(state="enabled")
            self.__start_time_entry_lable.config(state="disabled")
            self.__start_time_entry.config(state="disabled")
            self.__end_time_entry_label.config(state="disabled")
            self.__end_time_entry.config(state="disabled")
        elif self.__query_choice.get() == "Action Time":
            self.__action_menu_lable.config(state="disabled")
            self.__action_menu.config(state="disabled")
            self.__file_type_label.config(state="disabled")
            self.__file_type_entry.config(state="disabled")
            self.__file_directory_label.config(state="disabled")
            self.__file_directory_entry.config(state="disabled")
            self.__start_time_entry_lable.config(state="enabled")
            self.__start_time_entry.config(state="enabled")
            self.__end_time_entry_label.config(state="enabled")
            self.__end_time_entry.config(state="enabled")

    def spawn_report_generation(self):
        """Spawns a new window for report generation."""
        self.__report_generation_window = ReportGenerationFrame(
            self,
            self.__email_account,
            self.__email_password,
            self.__email_recipients,
            self.__report_file_name,
            self.__keep_report,
            self.__send_report_cmd,
        )
        self.__report_generation_window.grab_set()
        self.__report_generation_window.focus_set()


class QueryResultFrame(ttk.Frame):
    """
    A class used to represent a TableFrame which inherits from ttk.Frame and
    contains a table made out of tree widgets.


    Methods
    -------
    insert_row(self, values)
        Inserts a row into the table with the given values.
    clear_table(self)
        Clears all rows from the table.
    """

    def __init__(self, parent, columns):
        """
        Initializes the Treeview widget within a tkinter Frame.
        Args:
            parent (tkinter.Widget): The parent widget.
            columns (list): A list of column names for the Treeview.
        """

        super().__init__(parent)
        self.__tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.__tree.heading(col, text=col)
            self.__tree.column(col, anchor=tk.CENTER)
        self.__tree.pack(fill=tk.BOTH, expand=True)

    def insert_row(self, values):
        self.__tree.insert("", tk.END, values=values)

    def clear_table(self):
        for row in self.__tree.get_children():
            self.__tree.delete(row)


class ReportGenerationFrame(Toplevel):
    def __init__(
        self,
        parent,
        email_account: StringVar,
        email_password: StringVar,
        email_recipent: StringVar,
        report_file_name: StringVar,
        keep_report: BooleanVar,
        submit_action: Callable,
    ):
        super().__init__(parent, padx=10, pady=10)

        self.__report_file_name = report_file_name

        self.title("Generate Report of File Activity & Send By Email")
        self.geometry("500x400")
        ttk.Label(self, text="Enter From Email Account:").grid(row=0, column=1)
        ttk.Entry(self, textvariable=email_account).grid(row=0, column=3)

        ttk.Label(self, text="Enter Email Password:").grid(row=1, column=1)
        ttk.Entry(self, textvariable=email_password, show="*").grid(row=1, column=3)

        ttk.Label(self, text="Enter Email Recipient:").grid(row=2, column=1)
        ttk.Entry(self, textvariable=email_recipent).grid(row=2, column=3)

        self.__report_location_button = ActionButton(self, "Save Report As")
        self.__report_location_button.grid(row=3, column=1)
        self.__report_location_button.configure(command=self.save_report_dialog)
        ttk.Entry(self, textvariable=report_file_name).grid(row=3, column=3)
        ttk.Checkbutton(self, text="Keep The\nReport File", variable=keep_report).grid(
            row=3, column=4, pady=10
        )

        self.__submit_button = ActionButton(self, "Send Report")
        self.__submit_button.grid(row=10, column=1, padx=15, pady=15)
        self.__submit_button.config(command=lambda: submit_action())

    def save_report_dialog(self):
        fname = filedialog.asksaveasfilename(initialfile="file_activity_report.csv")
        self.__report_file_name.set(fname)

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
    def __init__(self, parent, exit_window):
        super().__init__(parent)
        self.exit_program = exit_window

    def exit_window(self):
        """On program exit, ask the user whether or not to write current contents to the database if those
        contents have not yet been written"""
        if messagebox.showinfo(
            "WARNING",
            "Do you want to quit?"):
            self.destroy()
        self.protocol("WM_DELETE_WINDOW", self.exit_window)

if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
