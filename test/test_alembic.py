import sqlite3
import unittest

from config import DB_ROOT


class TestAlembic(unittest.TestCase):
    def test_create_table(self):

        db_path = "{DB_ROOT}/{DB_NAME}".format(DB_ROOT=DB_ROOT, DB_NAME="git_slack.db")
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()

            table = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall()

            self.assertEqual(table[1][0], "repositories")
            self.assertEqual(table[2][0], "usernames")
            self.assertEqual(table[3][0], "pull_requests")


if __name__ == "__main__":
    unittest.main()
