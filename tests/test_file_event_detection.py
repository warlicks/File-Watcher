import os
import re
import shutil
import time
import pytest
from filewatch.file_watch import FileWatch


@pytest.fixture
def empty_dir_set_up():
    empty_path = "./tests/empty_dir"
    if os.path.exists(empty_path):
        shutil.rmtree(empty_path)
    os.mkdir(empty_path)
    yield empty_path

    shutil.rmtree(empty_path)


@pytest.fixture
def setup_directory_with_files():
    empty_path = "./tests/empty_dir/subdir"
    if os.path.exists(empty_path):
        shutil.rmtree(empty_path)
    os.makedirs(empty_path)
    dummy_file = os.path.join("./tests/empty_dir", "temp.txt")
    os.system(f"touch {dummy_file}")
    yield empty_path

    shutil.rmtree("./tests/empty_dir")


def test_new_file(empty_dir_set_up):
    """Test that creation of a new file is detected."""
    watcher = FileWatch()
    watcher.start_watching(empty_dir_set_up)

    os.system(f"touch {empty_dir_set_up + "/f1.txt"}")
    watcher.stop_watching()
    a = watcher.current_event

    assert a["event_type"] == "created"
    assert a["event_location"] == os.path.abspath(empty_dir_set_up)


def test_no_file_created(empty_dir_set_up):
    """Test that we don't get an event when no file is created."""
    watcher = FileWatch()
    watcher.start_watching(empty_dir_set_up)
    watcher.stop_watching()

    assert watcher.current_event is None


def test_new_file_with_existing_files(setup_directory_with_files):
    """Test creation detected when files are present in directory."""
    watcher = FileWatch()
    watcher.start_watching("./tests/empty_dir/")
    os.system("touch ./tests/empty_dir/file2.txt")
    watcher.stop_watching()

    a = watcher.current_event

    assert a["event_type"] == "created"


@pytest.mark.usefixtures("single_level_dir")
def test_specific_types(single_level_dir):
    """Test that we get can monitor specifc file types in the root of the monitored
    directory.
    Also demonstrates that other file types are properly ignored."""
    fname1 = os.path.join("./tests/rootdir/fake.py")
    fname2 = os.path.join("./tests/rootdir/fake.txt")
    fname3 = os.path.join("./tests/rootdir/fake.sql")
    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir", file_extension=[".txt", ".py"])

    os.system(f"touch {fname1}")
    os.system(f"touch {fname2}")
    os.system(f"touch {fname3}")

    watcher.stop_watching()
    print(watcher.event_history)
    assert len(watcher.event_history) == 2


@pytest.mark.usefixtures("single_sub_directory")
def test_recursive_file_creation(single_sub_directory):
    fname1 = "./tests/rootdir/level_0a/fake_file.txt"
    time.sleep(1)
    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir", True)

    os.system(f"touch {fname1}")
    time.sleep(1)

    watcher.stop_watching()

    assert len(watcher.event_history) == 1
    assert watcher.current_event["event_location"] == os.path.abspath(fname1)


def test_detect_directory_creation(single_level_dir):
    """Test that we can detect newly created directory"""
    dir_name = "./tests/rootdir/new_dir"
    time.sleep(1)
    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir/")

    os.system(f"mkdir {dir_name}")
    time.sleep(1)

    watcher.stop_watching()
    assert len(watcher.event_history) == 1
    assert watcher.current_event["event_location"] == os.path.abspath(dir_name)


def test_ignore_creation_in_parent_directory(single_sub_directory):
    """Test that file watcher ignores file creation in parent directory"""

    fname = "./tests/rootdir/new.py"
    time.sleep(0.5)
    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir/level_0a/")

    os.system(f"touch {fname}")
    time.sleep(0.25)

    watcher.stop_watching()
    assert not watcher.current_event
    assert not watcher.event_history
