import tkinter as tk
from tkinter import W, E, BooleanVar, StringVar, Toplevel, ttk, filedialog
from tkinter import font
from turtle import bgcolor
from typing import Callable
from .query_frame import QueryResultFrame, ActionButton


class WatcherFrame(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            text="Configure File Watching",
            labelanchor="n",
            borderwidth=5,
        )

        self.__directory_selection_frame = DirectorySelection(self)
        self.__directory_selection_frame.pack(pady=10)

        self.__frame_controls = ActionFrame(self)
        self.__frame_controls.pack(pady=5)

        self.__status_label = StatusLabel(self)
        self.__status_label.pack(pady=5)

        self.__change_log = QueryResultFrame(
            self, ["File", "Action", "Time", "File Type", "Move Destination"]
        )
        self.__change_log.pack()

    @property
    def selected_directory(self):
        return self.__directory_selection_frame.selected_directory

    @property
    def status_label(self):
        return self.__status_label

    @property
    def status_label_text(self):
        return self.__status_label.status_variable

    @property
    def start_button(self):
        return self.__frame_controls.start_button

    @property
    def stop_button(self):
        return self.__frame_controls.stop_button


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


class StatusLabel(ttk.Label):
    def __init__(self, parent):
        super().__init__(parent)

        self.__status_variable = StringVar()
        self.__status_variable.set("Status: Idle")
        self.configure(textvariable=self.__status_variable, foreground="blue")

    @property
    def status_variable(self):
        return self.__status_variable
