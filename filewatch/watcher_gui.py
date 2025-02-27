import tkinter as tk
from tkinter import W, E, N, S, StringVar, Toplevel, ttk, filedialog
from typing import Union, Callable


class WatcherGUI(tk.Tk):

    def __init__(self, controller=None):
        """_summary_

        _extended_summary_

        Args:
            controller (_type_, optional): _description_. Defaults to None.
        """
        super().__init__()

        self.title("File Watcher")
        self.geometry("600x400")

        self.directory_selection_frame = DirectorySelection(self)
        self.directory_selection_frame.pack(pady=10)
        self.__dir_to_watch = self.directory_selection_frame.selected_directory

        self.frame_controls = ActionFrame(self)
        self.frame_controls.pack(pady=5)

        # Create attributes for the start & stop buttons.
        # TODO: Refactor so the properties return these. We don't need to return @ this level to make them available to the ViewMangaer.
        self.__start_button = self.frame_controls.start_button
        self.__stop_button = self.frame_controls.end_button

        # Setup a button to open the query history window.
        self.new_window_button = ActionButton(self, "Query Change History")
        self.new_window_button.pack()
        self.new_window_button.configure(command=self.spawn_query_window)

        # Set Up Variables that need to be passed to the query window.
        self.__query_choice = StringVar()
        self.__query_string = StringVar()
        self.__query_results = StringVar()

        # We'll pass the search function "down" to the new window. Set via ViewManager.
        self.__search_function: Union[None | Callable] = None

        # define frame for query results to pass down to the query window.

    @property
    def start_button(self):
        return self.__start_button

    @property
    def stop_button(self):
        return self.__stop_button

    @property
    def dir_to_watch(self) -> str:
        return self.__dir_to_watch.get()

    @property
    def query_choice(self) -> StringVar:
        return self.__query_choice

    @property
    def query_string(self) -> StringVar:
        return self.__query_string

    @property
    def query_result(self) -> StringVar:
        return self.__query_results

    @property
    def search_function(self):
        return self.__search_function

    @search_function.setter
    def search_function(self, func: Callable):
        self.__search_function = func

    def spawn_query_window(self):
        # Use our getter methods to prevent access to internal attributes.
        self.__query_window = QueryWindow(
            self,
            self.query_choice,
            self.query_string,
            search_function=self.search_function,
        )


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
    def __init__(self, parent):
        super().__init__(parent)
        self.start_button = ActionButton(self, "Start Watching")
        self.start_button.pack(side=tk.LEFT, padx=5)
        self.end_button = ActionButton(self, "Stop Watching")
        self.end_button.pack(side=tk.LEFT, padx=5)


class ActionButton(tk.Button):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)


class QueryWindow(Toplevel):
    def __init__(
        self,
        parent,
        query_var: StringVar,
        query_string: StringVar,
        search_function: Callable,
    ):
        super().__init__(parent)
        self.title("Query Window")
        self.geometry("800x600")
        self.__query_var = query_var

        self.__query_frame = QueryFrame(
            self, self.query_var, query_string, search_function
        )
        self.__query_frame.pack()

        # Define Frame for Query Results
        ttk.Label(self, text="Query Resutls").pack(anchor=W, padx=5, pady=5)

        self.__query_result_frame = TableFrame(self, columns=["File", "Action", "Time"])
        self.__query_result_frame.pack(fill=tk.BOTH, expand=True)

    @property
    def query_var(self):
        return self.__query_var


class QueryFrame(ttk.Frame):
    def __init__(
        self,
        parent,
        query_var: StringVar,
        query_string: StringVar,
        search_function: Callable,
    ):
        super().__init__(parent, padding=(10, 10, 10, 10))
        self.__query_choice = query_var
        self.__query_string = query_string
        self.__label_query_option = ttk.Label(self, text="Select Query Option:")
        self.__label_query_option.grid(row=0, column=1, sticky=W)
        self.menu_wigit = tk.OptionMenu(
            self,
            self.__query_choice,
            "File Type",
            "File Action",
            "File Directory",
            "Action Time",
        )
        self.menu_wigit.grid(row=0, column=2, sticky=(W, E))
        ttk.Label(self, text="Enter Query String:").grid(
            row=1, column=1, sticky=W, padx=1, pady=5
        )
        ttk.Entry(self, textvariable=self.__query_string).grid(
            row=1, column=2, columnspan=2, rowspan=2, pady=5, sticky=(W, E)
        )
        self.__search_button = ActionButton(self, "Start Search")
        self.__search_button.config(command=search_function)
        self.__search_button.grid(row=3, column=2, pady=5, sticky=(W, E))


class TableFrame(ttk.Frame):
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
        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def insert_row(self, values):
        self.tree.insert("", tk.END, values=values)

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
