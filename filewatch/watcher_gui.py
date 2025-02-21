import tkinter as tk
from tkinter import ttk, filedialog


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

    @property
    def start_button(self):
        return self.__start_button

    @property
    def stop_button(self):
        return self.__stop_button

    @property
    def dir_to_watch(self):
        return self.__dir_to_watch.get()


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
        self.dir_entry = ttk.Entry(self, width=40)
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(self, text="Browse", command=self.select_directory).pack(
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


class ActionButton(ttk.Button):
    def __init__(self, parent, text):
        super().__init__(parent, text=text)


if __name__ == "__main__":
    g = WatcherGUI()
    g.mainloop()
