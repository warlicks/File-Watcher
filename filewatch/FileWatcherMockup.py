import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FileWatcherGUI:
    def __init__(self, root, database):
        self.root = root
        self.database = database

        root.title("FileWatcher GUI Mockup")
        root.geometry("600x400")
        root.protocol("WM_DELETE_WINDOW", on_exit)

        # Directory Selection
        frame_top = tk.Frame(root)
        frame_top.pack(pady=10)
        tk.Label(frame_top, text="Directory:").pack(side=tk.LEFT)
        self.dir_entry = tk.Entry(frame_top, width=40)
        self.dir_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(frame_top, text="Browse", command=select_directory).pack(side=tk.LEFT)

        # Extension Filter
        frame_ext = tk.Frame(root)
        frame_ext.pack(pady=5)
        tk.Label(frame_ext, text="Extension:").pack(side=tk.LEFT)
        self.ext_entry = tk.Entry(frame_ext, width=10)
        self.ext_entry.pack(side=tk.LEFT, padx=5)

        # Start/Stop Buttons
        frame_controls = tk.Frame(root)
        frame_controls.pack(pady=5)
        tk.Button(frame_controls, text="Start", command=start_watching).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_controls, text="Stop", command=stop_watching).pack(side=tk.LEFT, padx=5)

        # Log Panel
        log_frame = tk.Frame(root)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(log_frame, text="Log Panel:").pack(anchor=tk.W)
        self.log_text = tk.Text(log_frame, height=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)

        # Status Indicator
        status_label = tk.Label(root, text="Status: Idle", fg="blue")
        status_label.pack(pady=5)

    def select_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def start_watching(self):
        """Start watching selected directory and save to database"""
        directory = self.dir_entry.get()
        extension = self.ext_entry.get()

        if not directory or not extension:
            messagebox.showerror("Error", "Please select a directory and an extension")
            return

        self.db.insert_watched_directory(directory, extension)
        self.status_label.config(text="Status: Watching", fg="green")
        self.log_text.insert(tk.END, f"Watching {directory} for {extension} files\n")


    def stop_watching(self):
        """Stop watching selected directory and save to database"""
        self.status_label.config(text="Status: Stopped", fg="red")
        self.log_text.insert(tk.END, "Stopped watching. \n")

    def on_exit(self):
        """Message box s generated on exit of program"""
        messagebox.showinfo("Exit", "File Watching Application Closing.")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    database = FileWatcherDatabase
    app = FileWatcherGUI(root, database)
    root.mainloop()
