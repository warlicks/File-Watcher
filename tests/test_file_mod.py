import os
import time
import pytest
from filewatch.file_watch import FileHandler
from filewatch.watcher import FileWatcher


def test_opened_no_mod(single_level_dir):
    """Test ability to detect file opened and unmodified"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/test_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir")

    f = open(fname)
    time.sleep(0.25)
    f.close()
    time.sleep(0.25)
    watcher.stop_watching()

    assert watcher.handler.current_event["event_type"] == "closed_no_write"
    assert os.path.abspath(watcher.handler.current_event["event_location"]) == fname


def test_opened_no_mod_sub_dir(single_sub_directory):
    """Test ability to detect file opened and not modified in subdir."""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/level_0a/text_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir", recursive=True)

    f = open(fname)
    time.sleep(0.25)
    f.close()
    time.sleep(0.25)
    watcher.stop_watching()

    assert watcher.handler.current_event["event_type"] == "closed_no_write"
    assert os.path.abspath(watcher.handler.current_event["event_location"]) == fname


def test_opened_with_mod(single_level_dir):
    """Test ability to detect file opened and unmodified"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/test_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir")

    f = open(fname, "w+")
    f.write("Modifying the file :)")
    f.close()
    time.sleep(0.25)
    watcher.stop_watching()

    assert watcher.handler.current_event["event_type"] == "closed"
    assert os.path.abspath(watcher.handler.current_event["event_location"]) == fname
