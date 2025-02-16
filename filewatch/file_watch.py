import datetime
import os
import time
from watchdog.events import (
    DirCreatedEvent,
    DirDeletedEvent,
    DirModifiedEvent,
    DirMovedEvent,
    FileClosedEvent,
    FileClosedNoWriteEvent,
    FileCreatedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileOpenedEvent,
    FileSystemEvent,
    FileSystemEventHandler,
)

from typing import Union


class FileHandler(FileSystemEventHandler):

    def __init__(self) -> None:
        super().__init__()

        self.__current_event: Union[dict, None] = None
        self.__watched_extension: list = []
        self.__event_history = []
        self.__registered_observers = []

    @property
    def current_event(self) -> Union[dict, None]:
        return self.__current_event

    @property
    def event_history(self) -> list:
        return self.__event_history

    @property
    def watched_extension(self):
        return self.__watched_extension

    @watched_extension.setter
    def watched_extension(self, value: list):
        self.__watched_extension = value

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        """Watches for the creation of a file or directory.

        Args:
            event (DirCreatedEvent | FileCreatedEvent): A FileSystemEvent
            representing the creation of a file or directory.
            See https://python-watchdog.readthedocs.io/en/stable/api.html#watchdog.events.FileSystemEvent
        """
        if event.event_type == "created":
            file_type = os.path.splitext(event.src_path)
            if file_type[1] in self.__watched_extension or not self.__watched_extension:
                a = self._event_actions(event)
                print(a)

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
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

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent) -> None:
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

    def on_closed_no_write(self, event: FileClosedNoWriteEvent) -> None:
        if event.event_type == "closed_no_write":
            file_type = os.path.splitext(event.src_path)
            if file_type[1] in self.__watched_extension or not self.__watched_extension:
                a = self._event_actions(event)
                print(a)

    def on_closed(self, event: FileClosedEvent) -> None:
        if event.event_type == "closed":
            file_type = os.path.splitext(event.src_path)
            if file_type[1] in self.__watched_extension or not self.__watched_extension:
                a = self._event_actions(event)
                print(a)

    def _event_actions(self, event):
        """_summary_

        _extended_summary_

        Args:
            event (_type_): _description_

        Returns:
            _type_: _description_
        """
        if event.event_type == "moved":
            self.__current_event = {
                "event_type": event.event_type,
                "event_location": event.src_path,
                "file_destination": event.dest_path,
            }
        else:
            self.__current_event = {
                "event_type": event.event_type,
                "event_location": event.src_path,
                "event_sythetic": event.is_synthetic,
                "event_time": datetime.datetime.now(),
            }

        self.__event_history.append(self.__current_event)
        return self.__current_event

    def notify(self) -> None:
        pass
