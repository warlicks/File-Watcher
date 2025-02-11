import os
import shutil
import pytest
from filewatch.file_watch import FileWatch


@pytest.fixture
def test_dir_setup():
    path = "./test_files"
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir("./test_files")


def test_file_creation_detected(test_dir_setup):
    """Test that we can detect a file created in an empty directory."""

    watcher = FileWatch()
    watcher.start_watching("./test_files")

    os.system(f"touch {os.path.join("./test_files", "f1")}")
    watcher.stop_watching()
    a = watcher.current_event
    print(a)
    assert a["event_type"] == "created"
    assert a["event_location"] == os.path.abspath("./test_files")

    # os.rmdir("./test_files")
