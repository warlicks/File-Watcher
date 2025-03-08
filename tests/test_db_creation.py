from filewatch.file_database import FileWatcherDatabase
import datetime as dt


db = FileWatcherDatabase()
db.create_database_connection()
db.create_table()

fake_data = [
    {
        "event_time": dt.datetime(2023, 10, 1, 12, 00, 00),
        "event_type": "created",
        "event_location": "/path/to/file.txt",
        "file_type": ".txt",
        "move_destination": None,
    },
    {
        "event_time": dt.datetime(2023, 10, 1, 13, 00, 00),
        "event_type": "created",
        "event_location": "/path/to/file2.txt",
        "file_type": ".txt",
        "move_destination": None,
    },
    {
        "event_time": dt.datetime(2023, 10, 1, 13, 30, 00),
        "event_type": "moved",
        "event_location": "/path/to/file2.txt",
        "file_type": ".txt",
        "move_destination": "/path/to/new_dir/file2.txt",
    },
    {
        "event_time": dt.datetime(2023, 10, 1, 13, 45, 00),
        "event_type": "deleted",
        "event_location": "/path/to/new_dir/file2.txt",
        "file_type": ".txt",
        "move_destination": None,
    },
    {
        "event_time": dt.datetime(2023, 10, 1, 13, 45, 30),
        "event_type": "modified",
        "event_location": "/path/to/file1.sql",
        "file_type": ".sql",
        "move_destination": None,
    },
]

for data in fake_data:
    db.insert_data(
        int(data["event_time"].timestamp()),
        data["event_type"],
        data["event_location"],
        data["file_type"],
        data["move_destination"],
    )
