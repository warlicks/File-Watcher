import time
from watchdog.observers.polling import PollingObserver
from filewatch.file_watch import FileHandler


class FileWatcher:
    """Manages watching a file directory.

    The FileWatcher handles the actual watching for changes to a give directory
    set up. It schedules the watching, setting the directory, file types and if
    the monitoring should include sub-directories. It also starts and stops the
    monitoring process.

    The FileHandler needs a FileHandler to manage the detection and broadcasting
    of events.

    The FileWatcher uses a PollingObserver from the Watchdog package. The
    PollingObserver class is used because it provides consistent behaviors across
    operating systems.If you want to override this choice you need to inherit
    a new class.

    References:
    Watchdog Polling Observer: https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.observers.polling.PollingObserver

    """

    def __init__(self, handler: FileHandler):
        """Initialize a new FIleWatcher Instance


        Args:
            handler (FileHandler): A file handler that handles the identification,
              processing, and communication of changes to files in the monitored
              file directories.
        """
        self.__observer = PollingObserver()
        self.__handler = handler

    @property
    def handler(self):
        """Gets the current FileHandler"""
        return self.__handler

    def start_watching(
        self, directory: str = ".", recursive: bool = False, file_extension: list = []
    ):
        """Starts watching for file changes.

        Args:
            directory (str, optional): The directory that should be
              watched for file changes. Defaults to the current directory (aka ".").
            recursive (bool, optional): Determines if sub-directories should be
              watched. Defaults to False.
            file_extension (list, optional): A list of file extensions that
              should be monitored for changes. Defaults to all file extensions ([]).
        """
        self.__directory = directory
        self.__recursive = recursive
        self.__handler.watched_extension = file_extension
        self.__observer.schedule(self.__handler, directory, recursive=recursive)

        self.__observer.start()

    def stop_watching(self):
        """Stops watching for file changes"""
        print("Stopped Watching")

        self.__observer.stop()
        self.__observer.join()
