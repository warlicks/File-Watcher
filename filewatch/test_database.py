import os
import sqlite3
import time
from filewatch import file_database  # Adjust the import based on your file structure

# Initialize test database
db = file_database(database_directory=".", test_mode=True)
db.create_database_connection()
db.create_table()

# Function to reset the test database before running tests
def reset_test_database():
    """Deletes the test database if it exists to start fresh."""
    if os.path.exists("test_file_watch.db"):
        os.remove("test_file_watch.db")
    print("Test database reset.")

# Reset database before testing
reset_test_database()

# Reconnect after reset
db.create_database_connection()
db.create_table()

# Insert test data
event_time = int(time.time())
db.insert_data(event_time, "created", "/path/to/file1.txt", "txt", None)
db.insert_data(event_time, "modified", "/path/to/file2.py", "py", None)

# Test querying by file extension
print("\n🔹 Query by file extension (.txt):")
results = db.query_by_file_extension("txt")
for row in results:
    print(row)

# Test querying by event type
print("\n🔹 Query by event type (modified):")
results = db.query_by_event_type("modified")
for row in results:
    print(row)

# Test querying by event location
print("\n🔹 Query by event location (/path/to):")
results = db.query_by_event_location("/path/to")
for row in results:
    print(row)

# Test querying by event date
start_time = event_time - 1000
end_time = event_time + 1000
print("\n🔹 Query by event date range:")
results = db.query_by_event_date(start_time, end_time)
for row in results:
    print(row)

# Close connection
db.conn.close()
print("\n✅ Test database operations completed successfully.")
