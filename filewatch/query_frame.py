import tkinter as tk
from tkinter import W, E, BooleanVar, StringVar, Toplevel, ttk, filedialog
from typing import Callable


class ActionButton(tk.Button):
    def __init__(self, parent, text: str):
        """Creates action buttons.

        Wrapper around tk.Button

        Args:
            parent: Parent TK object.
            text (str): Text displayed in the button
        """
        super().__init__(parent, text=text)


class QueryWindow(tk.Frame):
    """Class for managing the GUI elements that allow user to query the database"""

    def __init__(self, parent):
        """Initializes an instance of the QueryWindow class
        Manages the query frame which allows the user to make a query of the database and
        displays the results.

        Args:
            parent: parent Tkinter object.
        """
        super().__init__(parent, borderwidth=1, relief="groove")

        tk.Label(
            self,
            text="Query File Change History",
            font=("Helvetica", "18", "bold underline"),
        ).pack(padx=5, pady=5)

        self.__query_frame = QueryFrame(self)
        self.__query_frame.pack()

        # Define Frame for Query Results
        ttk.Label(self, text="Query Results").pack(anchor=W, padx=5, pady=5)

        self.__query_result_frame = QueryResultFrame(
            self, columns=["File", "Action", "Time", "File Type", "Move Destination"]
        )
        self.__query_result_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.__query_frame.clear_button.configure(
            command=self.__query_result_frame.clear_table
        )

    @property
    def query_frame(self) -> "QueryFrame":
        """Gets frame for the user to select database query objects."""
        return self.__query_frame

    @property
    def query_result_frame(self) -> "QueryResultFrame":
        """Gets the gui frame that displays the database query results"""
        return self.__query_result_frame


class QueryFrame(ttk.Frame):

    def __init__(self, parent):
        """Initializes an instance of the QueryFrame class.

        Manages the frame and widgets that allow the user to select how they want to
        query the database and the specify the query criteria based on that choice.

        Args:
            parent: The parent Tkinter object.
        """
        super().__init__(parent)

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

        # Define Variables to Pass to the Report Generation Window. Need to be defined
        # here so they can be passed up and exposed to the controller layer.
        self.__email_account = StringVar()
        self.__email_password = StringVar()
        self.__email_recipients = StringVar()
        self.__report_file_name = StringVar()
        self.__keep_report = BooleanVar()
        self.__send_report_cmd = None

        ## Select the overall query approach.
        self.__label_query_option = ttk.Label(self, text="Select Query Option:")
        self.__label_query_option.grid(row=0, column=2, sticky=W)
        self.__menu_wigit = ttk.OptionMenu(
            self,
            self.__query_choice,
            "File Type",
            *menu_vals,
            command=lambda x: self.activate_query_optons(),
        )
        self.__menu_wigit.grid(row=0, column=3, sticky=(W, E))

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
        self.__clear_button = ActionButton(self, "Clear Results")
        self.__clear_button.grid(row=4, column=3, pady=5, sticky=(W, E))
        self.__generate_report_button = ActionButton(self, "Generate Report")
        self.__generate_report_button.config(
            command=lambda: self.spawn_report_generation()
        )
        self.__generate_report_button.grid(row=4, column=4, pady=5, sticky=(W, E))

    @property
    def search_button(self) -> ActionButton:
        """Returns the Button Widget for Starting the Search"""
        return self.__search_button

    @property
    def clear_button(self) -> ActionButton:
        """Returns the Clear Search Button Widget"""
        return self.__clear_button

    @property
    def query_choice(self) -> StringVar:
        """Returns the string variable indicating how the database will be searched."""
        return self.__query_choice

    @property
    def query_string(self) -> StringVar:
        """Returns the file extension for the database search"""
        return self.__query_string

    @property
    def query_action_type(self) -> StringVar:
        """Returns the file action type selected when querying by action type"""
        return self.__query_action_type

    @property
    def query_directory_string(self) -> StringVar:
        """Returns the string variable indicating how the database will be searched."""
        return self.__query_directory_sting

    @property
    def start_time_string(self) -> StringVar:
        """Returns the start timestamp when querying by time period"""
        return self.__start_time_string

    @property
    def end_time_string(self) -> StringVar:
        """Returns the end timestamp when querying by time period"""
        return self.__end_time_string

    @property
    def email_sender(self) -> StringVar:
        """Returns the string variable with the email senders email address"""
        return self.__email_account

    @property
    def email_password(self) -> StringVar:
        """Returns the password for the senders email account when sending a report."""
        return self.__email_password

    @property
    def email_recipients(self) -> StringVar:
        """Returns the email address of the report recipient"""
        return self.__email_recipients

    @property
    def report_file_name(self) -> StringVar:
        """Returns the full file name for the file activity report"""
        return self.__report_file_name

    @property
    def keep_report(self) -> BooleanVar:
        """Returns the boolean indicating if the report should be kept after being emailed."""
        return self.__keep_report

    @property
    def send_report_cmd(self):
        """Returns the send report command variable"""
        return self.__send_report_cmd

    @send_report_cmd.setter
    def send_report_cmd(self, value: Callable):
        """Sets the send report command"""
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

    def __init__(self, parent, columns):
        """Creates a frame to display results
        Initializes the Treeview widget within a tkinter Frame.

        Args:
          parent (tkinter.Widget): The parent object.
          columns (list): A list of column names for the result table.
        """

        super().__init__(parent)
        self.__tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.__tree.heading(col, text=col)
            self.__tree.column(col, anchor=tk.CENTER)
        self.__tree.pack(expand=True)

    def insert_row(self, values: tuple):
        """Inserts results into the table.

        Args:
            values (tuple): Values being inserted into the table. Values in the tuple
              should be in the order of the columns in the table.
        """
        self.__tree.insert("", tk.END, values=values)

    def clear_table(self):
        """Clears the table of any results presently displayed"""
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
        """Creates New Window to Manage Sending File Activity Report

        _extended_summary_

        Args:
            parent (_type_): Parent TK object
            email_account (StringVar): StringVar for the senders email address
            email_password (StringVar): StringVar for storing the senders email password.
            email_recipent (StringVar): StringVar for storing the recipient email address.
            report_file_name (StringVar): StringVar for storing the name of the
              activity report.
            keep_report (BooleanVar): BooleanVar indicating if the report file should be
              kept after being sent.
            submit_action (Callable): The method/function to be invoked when the submit
              button is pressed by the user.
        """
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
        """Opens file dialog for user to select where to save the file

        _extended_summary_
        """
        fname = filedialog.asksaveasfilename(initialfile="file_activity_report.csv")
        self.__report_file_name.set(fname)
