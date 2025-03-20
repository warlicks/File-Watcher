import os
import sqlite3
from sqlite3 import Error
from typing import Union


class FileWatcherDatabase:
    def __init__(
        self, database_directory: str = ".", database_name: str = "file_watch.db"
    ) -> None:
        """Creates a FileWatcherDatabase instance

        _extended_summary_

        Args:
            database_directory (str, optional): The directory where the database
              is stored. Defaults to users home directory (~).
            database_name (str, optional): The name of the database file. Defaults
              to 'file_watch.db'.
        """
        self.__database_location = os.path.join(
            os.path.abspath(database_directory), database_name
        )

    def create_database_connection(self) -> sqlite3.Connection:
        """Creates a connection to the database for the given instance

        Returns:
            sqlite3.Connection: A sqlite connection object to enable database actions in
            other methods.
        """
        try:
            conn = sqlite3.connect(self.__database_location)
            return conn
        except sqlite3.OperationalError as e:
            print(f"Failed to open {self.__database_location}")

    def create_table(self):
        """Creates table to hold file changes into the event."""
        try:
            c = self.create_database_connection().cursor()
            c.execute(self.__create_table_sql())
        except Error as e:
            print(e)
        finally:
            c.close()

    # I inadvertently just set the expectation that all time conversions will be done before
    # this function is called. I think this is a good idea. It means that the time conversion
    # is not tied to the database.
    def insert_data(
        self,
        event_time: int,
        event_type: str,
        event_location: str,
        file_type: str,
        move_destination: Union[str, None] = None,
    ):
        """
        Inserts data into the database.
        Args:
            event_time (int): The time of the event. The time should be in integer form
                (e.g., epoch time).
            event_type (str): The type of the event.
            event_location (str): The location of the event.
            file_type (str): The type of the file.
            move_destination (str, Optional): The destination where the file is moved. Defaults to None.
        Returns:
            None
        Raises:
            sqlite3.Error: If there is an error with the database operation.
        """
        try:
            conn = self.create_database_connection()
            c = conn.cursor()
            c.execute(
                self.__insert_data_sql(),
                (event_time, event_type, event_location, file_type, move_destination),
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def query_by_file_extension(self, ext_param: str) -> list:
        """Query the data base for changes that have to files with a given extension.

        Args:
            ext_param (str): The file extension of interest.

        Returns:
            list: Each item in the list is a database record matching the query condition
        """

        conn = self.create_database_connection()
        try:
            c = conn.cursor()
            c.execute(self.__file_extension_query(), (ext_param,))
            rows = c.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Query Error: {e}")
        finally:
            conn.close()

    def query_by_event_type(self, event_type: str) -> list:
        """Queries the database by event type.

        Args:
            event_type (str): The event type of interest.
        Returns:
            list: Each item in the list is a database record matching the query condition
        """
        conn = self.create_database_connection()
        try:
            c = conn.cursor()
            c.execute(self.__event_type_query(), (event_type,))
            rows = c.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def query_by_event_location(self, event_location: str) -> list:
        """Queries the database by event location.

        Args:
            event_location (str): The event location of interest.
        Returns:
            list: Each item in the list is a database record matching the query condition
        """
        conn = self.create_database_connection()
        try:
            c = conn.cursor()
            c.execute(self.__event_location_query(), ((f"{event_location}%",)))
            rows = c.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    def query_by_event_date(self, start_time: float, end_time: float) -> list:
        """Queries the database by event date.

        Args:
            start_time (int): The start time of interest. Should be in integer form
                (e.g., epoch time).
            end_time (int): The end time of interest. Should be in integer form
                (e.g., epoch time).
        Returns:
            list: Each item in the list is a database record matching the query condition
        """
        conn = self.create_database_connection()
        try:
            c = conn.cursor()
            c.execute(
                self.__event_date_query(),
                (
                    start_time,
                    end_time,
                ),
            )
            rows = c.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    # Queries are defined below. All queries are private methods that return the SQL as
    # a string. THe SQL must be parameterized.

    def __create_table_sql(self) -> str:
        """Holds query string for creating table."""

        sql = """
        CREATE TABLE If NOt EXISTS file_events (
	      "event_id"	INTEGER NOT NULL,
	      "event_time"	INTEGER NOT NULL,
	      "event_type"	TEXT NOT NULL,
	      "event_location"	TEXT NOT NULL,
	      "file_type"	INTEGER,
	      "move_destination"	TEXT,
	      PRIMARY KEY("event_id" AUTOINCREMENT)
        );
        """
        return sql

    def __insert_data_sql(self) -> str:
        """returns SQL query for inserting data into the file_events table"""
        return """
        
        INSERT INTO file_events (
            event_time,
            event_type,
            event_location,
            file_type,
            move_destination
        )
        VALUES (?, ?, ?, ?, ?)
        """

    def __file_extension_query(self) -> str:
        """returns SQL query for selecting by file extension"""
        sql = """
        SELECT
            event_location,
            event_type,
            event_time,
            file_type,
            move_destination

        FROM  file_events

        Where
            file_type = ?

        """
        return sql

    def __event_type_query(self) -> str:
        """returns SQL query for selecting by action type"""
        sql = """
        SELECT
            event_location,
            event_type,
            event_time,
            file_type,
            move_destination

        FROM  file_events

        Where
            event_type = ?
        """

        return sql

    def __event_location_query(self) -> str:
        """returns SQL query for selecting by event location"""
        sql = """
        
        SELECT
            event_location,
            event_type,
            event_time,
            file_type,
            move_destination

        FROM  file_events

        Where
            event_location like ?
        """
        return sql

    def __event_date_query(self) -> str:
        """returns SQL query for selecting by event date"""
        sql = """
        
        SELECT
            event_location,
            event_type,
            event_time,
            file_type,
            move_destination

        FROM  file_events

        Where
            event_time between ? and ?
        """
        return sql
