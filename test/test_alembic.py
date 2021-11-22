from enum import Enum
import sqlite3
import unittest

from config import DB_PATH


class Tables(Enum):
    REPOSITORIES = 1
    USERNAMES = 2
    PULL_REQUESTS = 3


class TestAlembic(unittest.TestCase):

    def test_create_table(self):

        db_path = DB_PATH.format(DB_NAME="git_slack.db")
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()

            table = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall()

            self.assertEqual(table[Tables.REPOSITORIES.value][0], "repositories")
            self.assertEqual(table[Tables.USERNAMES.value][0], "usernames")
            self.assertEqual(table[Tables.PULL_REQUESTS.value][0], "pull_requests")


if __name__ == "__main__":
    unittest.main()
