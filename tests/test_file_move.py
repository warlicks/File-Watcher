import time
import os
import pytest
from filewatch.file_watch import FileWatch


@pytest.mark.usefixtures("single_sub_directory")
def test_move_sub_directory(single_sub_directory):
    time.sleep(1)
    fname = "./tests/rootdir/test_0.ext"
    new_name = "./tests/rootdir/level_0a"

    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir", True)
    os.system(f"mv {fname} {new_name}")
    time.sleep(1)

    watcher.stop_watching()
    assert watcher.current_event["event_type"] == "moved"
    assert watcher.current_event["file_destination"] == os.path.abspath(
        os.path.join(new_name, "test_0.ext")
    )


@pytest.mark.usefixtures("single_sub_directory")
def test_move_to_unwatched_dir(single_sub_directory):
    time.sleep(1)
    fname = "./tests/rootdir/test_0.ext"
    new_name = "./tests/rootdir/level_0a"

    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir", False)
    os.system(f"mv {fname} {new_name}")
    time.sleep(1)

    watcher.stop_watching()
    assert watcher.current_event["event_type"] == "moved"


def test_moved_to_unwatched_parent(single_sub_directory):
    time.sleep(1)
    fname = "./tests/rootdir/level_0a/text_0.ext"
    new_name = "./tests/rootdir"

    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir")
    os.system(f"mv {fname} {new_name}")
    time.sleep(1)

    watcher.stop_watching()
    assert watcher.current_event["event_type"] == "moved"
    assert watcher.current_event["file_destination"] == os.path.abspath(
        "./tests/rootdir/text_0.ext"
    )
