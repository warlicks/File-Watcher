import os
import time
from xml.sax import handler
import pytest
from filewatch import watcher
from filewatch.file_watch import FileHandler
from filewatch.watcher import FileWatcher


class MockObserver:
    def __init__(self) -> None:
        pass

    def notify(self, current_event):

        print(f"{current_event["event_location"]} was {current_event["event_type"]}")


class MockObserverFail:
    def __init__(self) -> None:
        pass

    def another_method(self):
        pass


def test_observer_registration():
    """Test that we can register and deregister observers."""
    m = MockObserver()
    handler = FileHandler()
    handler.register_observers(m)

    assert len(handler.registered_observers) == 1
    assert handler.registered_observers[0] == m

    handler.deregister_observers(m)
    assert not handler.registered_observers


def test_observer_registration_rejected():
    m = MockObserverFail()
    handler = FileHandler()
    with pytest.raises(AttributeError):
        handler.register_observers(m)


def test_observer_notification_on_create(single_level_dir, capsys):
    """Test that observers are notified when"""
    m = MockObserver()
    h = FileHandler()
    h.register_observers(m)
    fname = "./tests/rootdir/new_file.txt"
    watcher = FileWatcher(h)
    watcher.start_watching("./tests/rootdir")

    os.system(f"touch {fname}")
    time.sleep(1)
    watcher.stop_watching()
    capture = capsys.readouterr()

    assert capture.out.startswith(f"{fname} was created")


def test_observer_notification_on_delete(single_level_dir, capsys):
    """Test that observers are notified when a deleted event happens"""
    m = MockObserver()
    fname = os.path.abspath("./tests/rootdir/test_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.handler.register_observers(m)
    watcher.start_watching("./tests/rootdir")

    os.system(f"rm {fname}")
    time.sleep(1)

    watcher.stop_watching()
    capture = capsys.readouterr()

    assert capture.out.startswith("./tests/rootdir/test_0.ext was deleted")


def test_observer_notification_on_move(single_sub_directory, capsys):
    """Test that observers are notified when a move event happens"""
    m = MockObserver()
    time.sleep(1)
    fname = "./tests/rootdir/test_0.ext"
    new_name = "./tests/rootdir/level_0a"

    watcher = FileWatcher(FileHandler())
    watcher.handler.register_observers(m)
    watcher.start_watching("./tests/rootdir", True)
    os.system(f"mv {fname} {new_name}")
    time.sleep(1)

    watcher.stop_watching()
    capture = capsys.readouterr()

    assert capture.out.startswith(f"{fname} was moved")


def test_observer_notification_on_modififed(single_level_dir, capsys):
    """Test that observers are notified when a modified event is triggered."""
    m = MockObserver()
    fname = "./tests/rootdir/test_0.py"
    watcher = FileWatcher(FileHandler())
    watcher.handler.register_observers(m)

    # Create a file we can write to via echo.
    os.system(f"touch {fname}")
    time.sleep(1)

    watcher.start_watching("./tests/rootdir")
    os.system(f"echo 'x=2\ny=3\nx_y' > {fname}")
    time.sleep(1)
    watcher.stop_watching()
    capture = capsys.readouterr()

    assert capture.out.startswith(f"{fname} was modified")
