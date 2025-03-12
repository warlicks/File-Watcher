import tkinter as tk
from tkinter import BooleanVar, StringVar, ttk, filedialog, W, E
from .query_frame import QueryResultFrame, ActionButton


class WatcherFrame(ttk.Frame):

    def __init__(self, parent):
        """_summary_

        _extended_summary_

        Args:
            parent: Parent TK object
        """
        super().__init__(parent)
        ttk.Label(
            text="Configure File Watcher Settings", style=self._lable_style()
        ).pack(pady=5, padx=5, anchor="center")

        self.__directory_selection_frame = DirectorySelection(self)
        self.__directory_selection_frame.pack(pady=10, anchor="center")

        self.__frame_controls = ActionFrame(self)
        self.__frame_controls.pack(pady=5)

        self.__status_label = StatusLabel(self)
        self.__status_label.pack(pady=5)

        self.__change_log = QueryResultFrame(
            self, ["File", "Action", "Time", "File Type", "Move Destination"]
        )
        self.__change_log.pack()

    @property
    def selected_directory(self) -> StringVar:
        """Returns the directory selected for monitoring"""
        return self.__directory_selection_frame.selected_directory

    @property
    def status_label(self) -> "StatusLabel":
        """Returns File Watcher Status Label"""
        return self.__status_label

    @property
    def status_label_text(self) -> StringVar:
        """Returns Status Label Text Variable"""
        return self.__status_label.status_variable

    @property
    def start_button(self) -> ActionButton:
        """Returns the Start Button Widget"""
        return self.__frame_controls.start_button

    @property
    def stop_button(self) -> ActionButton:
        """Returns the Stop Button Widget"""
        return self.__frame_controls.stop_button

    @property
    def file_ext_to_watch(self) -> str:
        """Returns the file extensions selected for monitoring"""
        self.__frame_controls.file_extension

    @property
    def recursive(self) -> bool:
        """Returns the boolean indicating if sub-directories should be monitored"""
        self.__frame_controls.recursive_monitor

    def _lable_style(self) -> str:
        """Internal method modifies ttk.Label style
        Returns:
          String with the name of the modified style
        """

        s = ttk.Style()
        s.configure("f.TLabel", font=("Helvetica", 18, "bold underline"))
        return "f.TLabel"


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

        self.__file_extension = StringVar()
        self.__recursive = BooleanVar()
        ttk.Label(self, text="Select File Extension:").grid(row=0, column=0)
        self.__file_ext_entry = ttk.Entry(self, textvariable=self.__file_extension)
        self.__file_ext_entry.grid(row=0, column=1)

        self.__recursive_box = ttk.Checkbutton(
            self, text="Monitor\nSub-Directories", variable=self.__recursive
        )
        self.__recursive_box.grid(row=0, column=2)

        self.start_button = ActionButton(self, "Start Watching")
        self.start_button.grid(row=1, column=1)

        self.stop_button = ActionButton(self, "Stop Watching")
        self.stop_button.grid(row=1, column=2)

    @property
    def file_extension(self) -> str:
        return self.__file_extension.get()

    @property
    def recursive_monitor(self) -> bool:
        return self.__recursive.get()


class StatusLabel(ttk.Label):
    def __init__(self, parent):
        super().__init__(parent)

        self.__status_variable = StringVar()
        self.__status_variable.set("Status: Idle")
        self.configure(textvariable=self.__status_variable, foreground="blue")

    @property
    def status_variable(self):
        return self.__status_variable
