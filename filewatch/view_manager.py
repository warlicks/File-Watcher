from .watcher import FileWatcher
#from filewatch.watcher import FileWatcher

from .watcher_gui import WatcherGUI


class ViewManager:
    def __init__(self, model: FileWatcher, view: WatcherGUI):
        self.__watcher = model
        self.__view = view

        self.__view.start_button.configure(command=self.send_start_watching)
        self.__view.stop_button.configure(command=self.send_stop_watching)

    def send_start_watching(self):
        print(f"Watching {self.__view.dir_to_watch}")
        self.__watcher.start_watching(
            self.__view.dir_to_watch,
        )

    def send_stop_watching(self):
        print(f"Stopped Watching {self.__view.dir_to_watch}")
        self.__watcher.stop_watching()
