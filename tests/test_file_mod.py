import os
import time
import pytest
from filewatch.file_watch import FileHandler
from filewatch.watcher import FileWatcher


def test_opened_no_mod(single_level_dir):
    """Test that we don't get a modified event w/o modification"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/test_0.ext")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir")

    f = open(fname)
    time.sleep(0.25)
    f.close()
    time.sleep(0.25)
    watcher.stop_watching()

    assert not watcher.handler.current_event
    assert not watcher.handler.event_history


def test_opened_no_mod_sub_dir(single_sub_directory: None):
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

    assert not watcher.handler.current_event
    assert not watcher.handler.event_history


def test_opened_with_mod(single_level_dir):
    """Test ability to detect file opened and unmodified"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/test_0.py")
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir")

    os.system(f"touch {fname}")
    time.sleep(1)
    os.system(f"echo 'x=2\ny=3\nx_y' > {fname}")
    time.sleep(1)
    watcher.stop_watching()

    assert watcher.handler.current_event["event_type"] == "modified"
    assert os.path.abspath(watcher.handler.current_event["event_location"]) == fname


def test_ignore_ds_store(single_level_dir):
    """Test ability to detect file opened and unmodified"""
    time.sleep(0.5)
    fname = os.path.abspath("./tests/rootdir/.DS_STORE")
    os.system(f"touch {fname}")
    time.sleep(1)
    watcher = FileWatcher(FileHandler())
    watcher.start_watching("./tests/rootdir")

    os.system(f"echo 'x=2\ny=3\nx_y' > {fname}")
    time.sleep(1)
    watcher.stop_watching()

    assert watcher.handler.current_event is None
