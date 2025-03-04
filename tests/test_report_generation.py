import os
from filewatch.view_manager import ViewManager
from filewatch.watcher import FileWatcher
from filewatch.file_watch import FileHandler
from filewatch.watcher_gui import WatcherGUI


def test_report_writing(single_level_dir):
    test_result = [
        ["path/to/file1.txt", "created", "2023-01-01 11:22:10", ".txt", None],
        ["path/to/file2.txt", "deleted", "2023-01-01 11:25:10", ".txt", None],
        ["path/to/file3.txt", "modified", "2023-01-01 11:22:20", ".txt", None],
    ]
    watcher = FileWatcher(FileHandler())
    vm = ViewManager(watcher, WatcherGUI())
    vm._write_report(test_result, "./tests/rootdir/test_report.csv")
    assert os.path.exists("./tests/rootdir/test_report.csv")
    with open("./tests/rootdir/test_report.csv", "r") as f:
        lines = f.readlines()
    assert len(lines) == 4
