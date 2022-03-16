import os
from typing import List, Tuple

import mysql.connector as sql
from dotenv import load_dotenv


class TestMysql:
    def __init__(self, table_name: str) -> None:
        """Intialize the connector and the cursor."""
        self.conn = None
        self.cursor = None
        self.table_name = table_name

    def connect_to_mysql_with_general_user(self) -> None:
        """Connect to MySQL as the user specified during docker build."""
        load_dotenv()

        HOST_NAME = os.getenv("DB_SERVICE_NAME")
        DB_NAME = os.getenv("DB_NAME")
        PASSWORD = os.getenv("DB_PASSWORD")
        DB_USER = os.getenv("DB_USER")
        DB_PORT = os.getenv("DB_PORT")

        self.conn = sql.connect(
            host=HOST_NAME, user=DB_USER, passwd=PASSWORD, port=DB_PORT, database=DB_NAME, charset="utf8mb4"
        )
        self.cursor = self.conn.cursor(buffered=True)

    def run_sql(self, query: str) -> None:
        """Run a query other than INSERT.

        Args:
            query(str): A query to run
        """
        self.cursor.execute(query)

    def run_sql_for_insert(self, query: str, data: Tuple[int, str]) -> None:
        """Run an INSERT query.

        Args:
            query(str): A query to run
        """
        self.cursor.execute(query, data)

    def create_table(self) -> None:
        """Create a table consisting of id and string."""
        query = f"create table if not exists {self.table_name} (id int, data varchar(20))"
        self.run_sql(query)

    def show_tables(self) -> List[Tuple[str]]:
        """Show tables in the database.

        Returns:
            List[Tuple[str,]]: Tables in the database.
        """
        query = "SHOW TABLES"
        self.run_sql(query)
        return self.cursor.fetchall()

    def insert_data(self, data: Tuple[int, str]) -> None:
        """Insert given data into the table.

        Args:
            data(Tuple[int, str]): Data consisting of id and string.
        """
        query = f"INSERT INTO {self.table_name} (id, data) VALUES (%s, %s)"
        self.run_sql_for_insert(query, data)

    def delete_data(self) -> None:
        """Delete data in the table."""
        query = f"TRUNCATE TABLE {self.table_name}"
        self.run_sql(query)

    def select_data(self) -> List[Tuple[int, str]]:
        """Retrieve data from the table.

        Returns:
            List[Tuple[int, str]]: Data to retrieve from the table.
        """
        query = f"SELECT * FROM {self.table_name}"
        self.run_sql(query)
        return self.cursor.fetchall()

    def count_data(self) -> int:
        """Count the number of data in the previous SQL operation.

        Returns:
            int: The number of data.
        """
        return self.cursor.rowcount

    def drop_table(self) -> None:
        """Drop table in the database."""
        query = f"DROP TABLE IF EXISTS {self.table_name}"
        self.run_sql(query)

    def rollback(self) -> None:
        """Rollback SQL operations."""
        self.close_cursor()
        self.conn.rollback()
        self.close_conn()

    def commit(self) -> None:
        """Commit SQL operations."""
        self.conn.commit()

    def close(self) -> None:
        """Close the connector and the cursor."""
        self.close_cursor()
        self.conn.close()

    def close_conn(self) -> None:
        """Close the connector."""
        self.conn.close()

    def close_cursor(self) -> None:
        """Close the cursor."""
        self.cursor.close()


def test_mysql_operations(table_name: str) -> None:
    """Test connection to MySQL and various MySQL operations.

    Args:
        table_name(str): Table name used to check MySQL operations.
    """
    test_mysql = TestMysql(table_name)

    try:
        test_mysql.connect_to_mysql_with_general_user()
        test_mysql.drop_table()
        test_mysql.create_table()
        assert test_mysql.show_tables() == [(table_name,)], "Failed to create table."

        data = (1, "test message")
        test_mysql.insert_data(data)
        assert test_mysql.count_data() == 1, "Failed to insert data."
        assert test_mysql.select_data() == [data], "Failed to retrieve data"

        test_mysql.delete_data()
        assert test_mysql.count_data() == 0, "Failed to delete data."

        test_mysql.drop_table()
        assert test_mysql.show_tables() == [], "Failed to drop table."

        test_mysql.commit()
        test_mysql.close()
    except:
        test_mysql.rollback()
        raise RuntimeError("An error occurred during SQL processing.")


if __name__ == "__main__":
    table_name = "test_table"
    test_mysql_operations(table_name)
