import os
from watchdog.events import (
    DirCreatedEvent,
    DirMovedEvent,
    FileCreatedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer
from typing import Union


class FileWatch(FileSystemEventHandler):

    def __init__(self) -> None:
        super().__init__()

        self.__observer = Observer()
        self.__current_event: Union[dict, None] = None
        self.__watched_extension: Union[list, None] = []
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
        return self.__watched_extensions

    @watched_extension.setter
    def watched_extension(self, values: list) -> None:
        self.__watched_extensions = values

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        file_type = os.path.splitext(event.src_path)
        if file_type[1] in self.__watched_extension or not self.__watched_extension:
            print("Watching this file type")
            a = self._event_actions(event)
            print(a)
        else:
            print("ignoring this filetype ")
        # self._event_actions(event)

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        self._event_actions(event)

    def _event_actions(self, event):
        """Internal method for"""
        self.__current_event = {
            "event_type": event.event_type,
            "event_location": event.src_path,
        }
        self.__event_history.append(self.__current_event)
        return self.__current_event

    def start_watching(
        self, dir: str, recursive: bool = False, file_extension=[]
    ) -> None:
        self.__watched_extension = file_extension
        self.__observer.schedule(self, dir, recursive=recursive)
        self.__observer.start()

        print(f"Watching {dir}")

    def stop_watching(self) -> None:
        self.__observer.stop()
        self.__observer.join()
        print("Stopped_watching")

    def notify(self) -> None:
        pass
