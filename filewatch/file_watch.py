import datetime
import os
import datetime as dt
from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)

from typing import Union, List


class FileHandler(FileSystemEventHandler):
    """Detects and reports on changes to files.

    Filehandler is used to detect the creation, deletion, movement and
    modification of files. Filehandler inherits from the watchdog package's
    FileSystemEventHandler. As a result the methods defined here wrap the methods
    defined in the Base Class.

    When actions are taken on files or directory, it is not uncommon for multiple
    events to be detected. For example when creating a "created" event for the file
    happens and "modified" event for the directory triggers. FileHandler eliminates
    the redundant directory level events and only return the event that best
    defines the event. When a file is created only the "created" event is recorded
    by FileHandler.


    References:
    Watchdog https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.events.FileSystemEvent
    """

    def __init__(self) -> None:
        """Creates an instance of the FileHandler"""
        super().__init__()

        self.__current_event: Union[dict, None] = None
        self.__watched_extension: list = []
        self.__event_history = []
        self.__registered_observers = []

    @property
    def current_event(self) -> Union[dict, None]:
        """Gets the most recently detected file system event

        When an event is detected the following information is recorded.
        1. Event Type (str)
        2. Event Location (str)
        3. File Type (str)
        3. Event Time (as a string)
        4. If it is a directory event (boolean)
        5. File Destination (Only if a move event)

        Returns:
            Union[dict, None]: If an event has occurred a dictionary with
              information about the event are returned. None is returned if no
              events have been detected.
        """
        return self.__current_event

    @property
    def event_history(self) -> List[Union[dict, None]]:
        """Gets the record of all the events that have occurred.

        Returns:
            List[Union[dict, None]]: Each item in the list is a dictionary
              containing information about all detected events. If no events have
              been detected the list will be empty.

        See Also:
          :func: ` current_event <file_watch.FileHandler.current_event>`
        """

        return self.__event_history

    @property
    def watched_extension(self) -> List[str]:
        """The get or set the file extensions that FileWatcher should monitor.

        If specific file types are not indicated, all file types are watched.

        Returns:
            list: A list with each element being a file extension.
        """
        return self.__watched_extension

    @watched_extension.setter
    def watched_extension(self, value: list):
        self.__watched_extension = value

    def on_created(self, event: Union[DirCreatedEvent, FileCreatedEvent]) -> None:
        """Watches for the creation of a file or directory.

        Args:
            event (DirCreatedEvent | FileCreatedEvent): A FileSystemEvent
            representing the creation of a file or directory.
            See https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.events.FileSystemEvent
        """
        if event.event_type == "created":
            file_type = os.path.splitext(event.src_path)
            if file_type[1] in self.__watched_extension or not self.__watched_extension:
                temp = {
                    "event_type": event.event_type,
                    "event_location": event.src_path,
                    "dir_event": event.is_directory,
                    "event_time": dt.datetime.now(),
                }
                # TODO: refactor this to take an event.
                self._reconcile_created_events(temp)
                self.notify()

    def on_moved(self, event: Union[DirMovedEvent, FileMovedEvent]) -> None:
        """Watches for file or directory being moved.

        Args:
            event (DirMovedEvent | FileMovedEvent): A FileSystemEvent
            representing the moving of a file or directory.
            See https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.events.FileSystemEvent
        """
        # With a modified event present we get a bunch of extra event calls. We
        # Need to filter to just the created event!
        if event.event_type == "moved":
            file_type = os.path.splitext(event.src_path)
            if file_type[1] in self.__watched_extension or not self.__watched_extension:
                self._event_actions(event)

    def on_deleted(self, event: Union[DirDeletedEvent, FileDeletedEvent]) -> None:
        """Watches for file or directory being deleted.

        Args:
            event (DirMovedEvent | FileMovedEvent): A FileSystemEvent
            representing the moving of a file or directory.
            See https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.events.FileSystemEvent
        """
        file_type = os.path.splitext(event.src_path)
        if file_type[1] in self.__watched_extension or not self.__watched_extension:
            a = self._event_actions(event)
            print(a)

    def on_modified(self, event: Union[DirModifiedEvent, FileModifiedEvent]) -> None:
        """Watches for file or directory being modified.

        Args:
            event (DirMovedEvent | FileMovedEvent): A FileSystemEvent
            representing the moving of a file or directory.
            See https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.events.FileSystemEvent
        """
        file_type = os.path.splitext(event.src_path)

        if file_type[1] in self.__watched_extension or not self.__watched_extension:

            temp = {
                "event_type": event.event_type,
                "event_location": event.src_path,
                "dir_event": event.is_directory,
                "event_time": dt.datetime.now(),
            }
            self._reconcile_modified_events(temp)

    def _reconcile_modified_events(self, temp: dict):
        """Determines if a modified event was triggered by another event

        When files are created, deleted or moved, a modified event for the directory also
        fires. The modified event fires after the file event. The since the modified
        events are redundant we filter them out.

        The redundant events are filtered out if the the previous event in the event history
        is a created, deleted or moved event, the current event is a modified event

        Args:
            temp (dict): _description_
        """
        # TODO: Refactor this so _reconcile_modified event takes the event as argument.
        if self.__event_history:
            previous_event = self.__event_history[-1]
            if (
                (
                    previous_event["event_type"] == "created"
                    or previous_event["event_type"] == "deleted"
                    or previous_event["event_type"] == "moved"
                )
                # and temp["dir_event"]
                and (temp["event_time"] - previous_event["event_time"])
                < dt.timedelta(milliseconds=500)
            ):
                return
            else:
                self.__event_history.append(temp)
                self.__current_event = temp
        else:
            self.__event_history.append(temp)
            self.__current_event = temp

    def _reconcile_created_events(self, temp):
        """Determines if a created event was triggered by another event

        When a directory is created, a modified event for the parent directory also
        fires. The modified event fires before the created event. The since the modified
        events are redundant we filter them out.

        The redundant events are filtered out if the the previous event in the event history
        is a created, deleted or moved event, the current event is a modified event

        Args:
            temp (dict): _description_
        """
        if self.__event_history:
            previous_event = self.__event_history[-1]
            if (
                previous_event["event_type"] == "modified"
                and previous_event["dir_event"]
                and (temp["event_time"] - previous_event["event_time"])
                < dt.timedelta(milliseconds=500)
            ):
                self.__event_history.pop()
                self.__event_history.append(temp)
                self.__current_event = temp
            elif previous_event["event_type"] == "created":
                self.__event_history.append(temp)
                self.__current_event = temp
            else:
                return
        else:
            self.__event_history.append(temp)
            self.__current_event = temp

    def _event_actions(self, event):
        """Internal method for processing event information

        Creates a dictionary with the event information. Adds it to the event
        history and sets it as the current event

        Args:
            event (): event from one of the "on" methods.

        """
        if event.event_type == "moved":
            self.__current_event = {
                "event_type": event.event_type,
                "event_location": event.src_path,
                "file_destination": event.dest_path,
                "dir_event": event.is_directory,
                "event_time": datetime.datetime.now(),
            }
        else:
            self.__current_event = {
                "event_type": event.event_type,
                "event_location": event.src_path,
                "event_time": datetime.datetime.now(),
            }

        self.__event_history.append(self.__current_event)
        return self.__current_event

    def register_observers(self, observer):
        self.__registered_observers.append(observer)

    def deregister_observers(self, observer):
        self.__registered_observers.remove(observer)

    def notify(self) -> None:
        for observer in self.__registered_observers:
            observer.notify(self.current_event)
