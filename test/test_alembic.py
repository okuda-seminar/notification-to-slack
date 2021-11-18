import sqlite3
import unittest

import pandas as pd

from config import DB_PATH


class TestAlembic(unittest.TestCase):
    def test_create_table(self):

        db_path = DB_PATH.format(DB_NAME="git_slack.db")
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()

            table = cursor.execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall()

            idx_df = pd.DataFrame(
                    dict(REPOSITORIES_IDX=[1], USERNAMES_IDX=[2], PULL_REQUESTS_IDX=[3])
                    )

            self.assertEqual(table[idx_df.REPOSITORIES_IDX.values[0]][0], "repositories")
            self.assertEqual(table[idx_df.USERNAMES_IDX.values[0]][0], "usernames")
            self.assertEqual(table[idx_df.PULL_REQUESTS_IDX.values[0]][0], "pull_requests")


if __name__ == "__main__":
    unittest.main()
