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

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        """_summary_

        _extended_summary_

        Args:
            event (DirCreatedEvent | FileCreatedEvent): _description_
        """
        file_type = os.path.splitext(event.src_path)
        if file_type[1] in self.__watched_extension or not self.__watched_extension:
            a = self._event_actions(event)

    def on_moved(self, event: DirMovedEvent | FileMovedEvent) -> None:
        """_summary_

        _extended_summary_

        Args:
            event (DirMovedEvent | FileMovedEvent): _description_
        """
        file_type = os.path.splitext(event.src_path)
        if file_type[1] in self.__watched_extension or not self.__watched_extension:
            self._event_actions(event)

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
            }

        self.__event_history.append(self.__current_event)
        return self.__current_event

    def start_watching(
        self, dir: str, recursive: bool = False, file_extension=[]
    ) -> None:
        """_summary_

        _extended_summary_

        Args:
            dir (str): _description_
            recursive (bool, optional): _description_. Defaults to False.
            file_extension (list, optional): _description_. Defaults to [].
        """
        self.__watched_extension = file_extension
        self.__observer.schedule(self, dir, recursive=recursive)
        self.__observer.start()

        print(f"Watching {dir}")

    def stop_watching(self) -> None:
        """_summary_

        _extended_summary_
        """
        self.__observer.stop()
        self.__observer.join()
        print("Stopped_watching")

    def notify(self) -> None:
        pass
