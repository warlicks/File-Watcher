import tkinter as tk
from tkinter import StringVar, Toplevel, ttk, filedialog
from typing import Union, Callable


class WatcherGUI(tk.Tk):

    def __init__(self):
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
            query_results=self.query_result,
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
        query_results: StringVar,
    ):
        super().__init__(parent)
        self.title("Query Window")
        self.geometry("600x400")
        self.__query_var = query_var

        self.__query_frame = QueryFrame(
            self, self.query_var, query_string, search_function
        )
        self.__query_frame.pack()

        self.__query_result_frame = QueryResultFrame(self, query_results)
        self.__query_result_frame.pack()

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
        super().__init__(parent)
        self.__query_choice = query_var
        self.__query_string = query_string
        self.menu_wigit = tk.OptionMenu(
            self,
            self.__query_choice,
            "File Type",
            "File Action",
            "File Directory",
        )
        self.menu_wigit.pack()
        label_test = ttk.Label(self, textvariable=self.__query_choice)
        label_test.pack(side=tk.LEFT)
        tk.Entry(self, textvariable=self.__query_string).pack(side=tk.LEFT, padx=10)
        self.__search_button = ActionButton(self, "Start Search")
        self.__search_button.config(command=search_function)
        self.__search_button.pack()


class QueryResultFrame(ttk.Frame):
    def __init__(self, parent, query_results: StringVar):
        super().__init__(parent)

        ttk.Label(self, text="Query Results").pack(anchor=tk.W)
        log_text = ttk.Label(self, textvariable=query_results)
        log_text.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
