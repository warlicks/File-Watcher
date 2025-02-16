import os
import pytest
import time

from filewatch.watcher import FileWatcher
from filewatch.file_watch import FileHandler


def test_file_deletion(single_level_dir):
    """Test ability to detect file removal"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/test_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir")

    os.system(f"rm {fname}")
    time.sleep(1)
    watcher.stop_watching()

    assert watcher.handler.current_event["event_type"] == "deleted"
    assert os.path.abspath(watcher.handler.current_event["event_location"]) == fname


def test_file_deletion_specific_ext(single_level_dir):
    """Test that deletion of unwatched extensions are ignored"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/test_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir", file_extension=[".py"])

    os.remove(fname)
    time.sleep(0.5)

    watcher.stop_watching()

    assert not watcher.handler.current_event
    assert not watcher.handler.event_history


def test_file_deletion_subdir(single_sub_directory):
    """Test that deletion of file in sub-directory is detected with recursive watch"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/level_0a/text_0.ext")
    watcher = FileWatcher(FileHandler())

    watcher.start_watching("./tests/rootdir", True)

    os.system(f"rm {fname}")
    time.sleep(1)

    watcher.stop_watching()

    assert watcher.handler.current_event["event_type"] == "deleted"
    assert os.path.abspath(watcher.handler.current_event["event_location"]) == fname


def test_file_deletion_subdir_ignore(single_sub_directory):
    """Test that deletion of file in sub-directory is ignored w/o recursive watch"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/level_0a/text_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir", False)

    os.remove(fname)
    time.sleep(0.5)

    watcher.stop_watching()

    assert not watcher.handler.current_event
    assert not watcher.handler.event_history


def test_file_deletion_in_parent_dir(single_sub_directory):
    """Test that deletion of file in sub-directory is ignored w/o recursive watch"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/test_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir/level_0a", False)

    os.remove(fname)
    time.sleep(0.5)

    watcher.stop_watching()

    assert not watcher.handler.current_event
    assert not watcher.handler.event_history
