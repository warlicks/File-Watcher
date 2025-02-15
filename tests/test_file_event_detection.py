import os
import shutil
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
    watcher = FileWatch()
    watcher.start_watching(empty_dir_set_up)

    os.system(f"touch {empty_dir_set_up + "/f1.txt"}")
    watcher.stop_watching()
    a = watcher.current_event

    assert a["event_type"] == "created"
    assert a["event_location"] == os.path.abspath(empty_dir_set_up)


def test_no_file_created(empty_dir_set_up):
    watcher = FileWatch()
    watcher.start_watching(empty_dir_set_up)
    watcher.stop_watching()

    assert watcher.current_event is None


def test_new_file_with_existing_files(setup_directory_with_files):
    watcher = FileWatch()
    watcher.start_watching("./tests/empty_dir/")
    os.system("touch ./tests/empty_dir/file2.txt")
    watcher.stop_watching()

    a = watcher.current_event

    assert a["event_type"] == "created"
    # assert a["event_location"] == os.path.abspath("./tests/empty_dir/file2.txt")


# good test to write, monitor sub directory & change in parent directory. Should not find a change !


@pytest.mark.usefixtures("single_level_dir")
def test_specific_types(single_level_dir):
    fname1 = os.path.join("./tests/rootdir/fake2.txt")
    fname2 = os.path.join("./tests/rootdir/fake.txt")
    fname3 = os.path.join("./tests/rootdir/fake.sql")
    watcher = FileWatch()
    watcher.start_watching("./tests/rootdir", file_extension=[".txt"])

    os.system(f"touch {fname1}")
    os.system(f"touch {fname2}")
    os.system(f"touch {fname3}")

    watcher.stop_watching()
    print(watcher.event_history)
    assert len(watcher.event_history) == 2
