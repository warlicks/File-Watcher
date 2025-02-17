import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def select_directory():
    directory = filedialog.askdirectory()
    if directory:
        dir_entry.delete(0, tk.END)
        dir_entry.insert(0, directory)

def start_watching():
    status_label.config(text="Status: Watching", fg="green")

def stop_watching():
    status_label.config(text="Status: Stopped", fg="red")

def on_exit():
    messagebox.showinfo("Exit", "File Watching Application Closing.")
    root.destroy()

root = tk.Tk()
root.title("FileWatcher GUI Mockup")
root.geometry("600x400")
root.protocol("WM_DELETE_WINDOW", on_exit)

# Directory Selection
frame_top = tk.Frame(root)
frame_top.pack(pady=10)
tk.Label(frame_top, text="Directory:").pack(side=tk.LEFT)
dir_entry = tk.Entry(frame_top, width=40)
dir_entry.pack(side=tk.LEFT, padx=5)
tk.Button(frame_top, text="Browse", command=select_directory).pack(side=tk.LEFT)

# Extension Filter
frame_ext = tk.Frame(root)
frame_ext.pack(pady=5)
tk.Label(frame_ext, text="Extension:").pack(side=tk.LEFT)
ext_entry = tk.Entry(frame_ext, width=10)
ext_entry.pack(side=tk.LEFT, padx=5)

# Start/Stop Buttons
frame_controls = tk.Frame(root)
frame_controls.pack(pady=5)
tk.Button(frame_controls, text="Start", command=start_watching).pack(side=tk.LEFT, padx=5)
tk.Button(frame_controls, text="Stop", command=stop_watching).pack(side=tk.LEFT, padx=5)

# Log Panel
log_frame = tk.Frame(root)
log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
tk.Label(log_frame, text="Log Panel:").pack(anchor=tk.W)
log_text = tk.Text(log_frame, height=10)
log_text.pack(fill=tk.BOTH, expand=True)

# Status Indicator
status_label = tk.Label(root, text="Status: Idle", fg="blue")
status_label.pack(pady=5)

root.mainloop()
