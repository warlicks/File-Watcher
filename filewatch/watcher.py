import time
from watchdog.observers.polling import PollingObserver
from filewatch.file_watch import FileHandler


class FileWatcher:
    def __init__(self, handler: FileHandler):
        self.__observer = PollingObserver()
        self.__handler = handler

    @property
    def handler(self):
        return self.__handler

    def start_watching(
        self, directory: str = ".", recursive: bool = False, file_extension: list = []
    ):
        self.__directory = directory
        self.__recursive = recursive
        self.handler.watched_extension = file_extension
        self.__observer.schedule(self.__handler, directory, recursive=recursive)

        self.__observer.start()

    def stop_watching(self):
        print("Stopped Watching")

        self.__observer.stop()
        self.__observer.join()
