import tkinter as tk
from tkinter import StringVar, Toplevel, ttk, filedialog


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

        self.__start_button = self.frame_controls.start_button
        self.__stop_button = self.frame_controls.end_button

        self.new_window_button = ActionButton(self, "Query Change History")
        self.new_window_button.pack()
        self.new_window_button.configure(command=self.spawn_query_window)

        # We define this here so we can pass it to the Query window when it is spawned on the button click.
        # TODO: Assign the other variables that need to pass back up from the new window
        # TODO: Create the start search button and pass it down so it can be accessed from the main window
        self.__query_choice = StringVar()

    @property
    def start_button(self):
        return self.__start_button

    @property
    def stop_button(self):
        return self.__stop_button

    @property
    def dir_to_watch(self):
        return self.__dir_to_watch.get()

    @property
    def query_choice(self):
        return self.__query_choice

    def spawn_query_window(self):
        QueryWindow(self, self.query_choice)


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
    def __init__(self, parent, query_var):
        super().__init__(parent)
        self.title("Query Window")
        self.geometry("600x400")
        self.__query_var = query_var

        self.query_frame = QueryFrame(self, self.query_var)
        self.query_frame.pack()

    @property
    def query_var(self):
        return self.__query_var


class QueryFrame(ttk.Frame):
    def __init__(self, parent, query_var):
        super().__init__(parent)
        self.__query_choice = query_var
        self.__query_label_text = StringVar()
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
        tk.Entry(self).pack(side=tk.LEFT, padx=10)
        self.__search_button = ActionButton(self, "Start Search")
        self.__search_button.pack()

    @property
    def query_choice(self):
        return self.__query_choice

    def query_entry_text(self):
        if self.__query_choice.get() == "File Type":
            self.__query_label_text.set("Search For File Extension")
        elif self.__query_choice.get() == "File Action":
            self.__query_label_text.set("Search For File Action")
        elif self.__query_choice.get() == "File Directory":
            self.__query_label_text.set("Search By File Directory")


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
