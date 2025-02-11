from watchdog.events import DirCreatedEvent, FileCreatedEvent, FileSystemEventHandler
from watchdog.observers import Observer
from typing import Union


class FileWatch(FileSystemEventHandler):

    def __init__(self) -> None:
        super().__init__()

        self.__observer = Observer()
        self.__current_event: Union[dict, None] = None
        self.__event_history = []

    @property
    def current_event(self) -> Union[dict, None]:
        return self.__current_event

    @property
    def event_history(self) -> list:
        return self.__event_history

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
        self.__current_event = {
            "event_type": event.event_type,
            "event_location": event.src_path,
        }
        self.__event_history.append(self.current_event)

    def start_watching(self, dir: str, recursive: bool = False) -> None:
        self.__observer.schedule(self, dir, recursive=recursive)
        self.__observer.start()

    def stop_watching(self) -> None:
        self.__observer.stop()

    def notify(self) -> None:
        pass
