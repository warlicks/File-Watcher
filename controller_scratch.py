"""SCRATCH FILE FOR Playing With the File Watcher Program!

This could form the basis for the main program or we could throw it away
"""

from filewatch import watcher
from filewatch.watcher_gui import WatcherGUI
from filewatch.view_manager import ViewManager
from filewatch.file_watch import FileHandler
from filewatch.watcher import FileWatcher

gui = WatcherGUI()
watch = FileWatcher(FileHandler())
controller = ViewManager(watch, gui)

gui.mainloop()
