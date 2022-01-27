from os.path import join
import unittest
import sqlite3
from datetime import datetime, timedelta
from enum import IntEnum

from config.const import DB_ROOT
from src.register_pr import create_table, insert_data

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class CreateTableNum(IntEnum):
    # table = [("pull_requests",),("sqlite_sequence",),("repositories",)]
    PULL_REQUESTS_NUM = 0
    REPOSITORIES_NUM = 2


class InsertDataNum(IntEnum):
    PR_TITLE_NUM = 1
    REPOSITORY_TITLE_NUM = 2
    TIME_CREATED_NUM = 3
    TIME_UPDATED_NUM = 4
    TIME_NOW_NUM = 5


class TestRegisterPr(unittest.TestCase):

    def test_create_table(self):
        """Test create_table function
        """
        db_path = join(DB_ROOT, "test.db")
        create_table(db_path)
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            table = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            self.assertEqual(table[CreateTableNum.PULL_REQUESTS_NUM][0], "pull_requests")
            self.assertEqual(table[CreateTableNum.REPOSITORIES_NUM][0], "repositories")

    def test_insert_data(self):
        """Test insert_data function
        """
        db_path = join(DB_ROOT, "test.db")
        insert_data(db_path)
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            repositories = cursor.execute("SELECT * FROM repositories").fetchall()
            self.assertIsNotNone(repositories)
            pull_requests = cursor.execute("SELECT * FROM pull_requests").fetchall()
            pr_list = [pr[InsertDataNum.PR_TITLE_NUM] for pr in pull_requests]
            pr_list = list(set(pr_list))
            for repository in repositories:
                created_time = datetime.strptime(repository[InsertDataNum.TIME_CREATED_NUM], TIME_FORMAT)
                updated_time = datetime.strptime(repository[InsertDataNum.TIME_UPDATED_NUM], TIME_FORMAT)
                one_day_deltatime = datetime.strptime(repository[InsertDataNum.TIME_NOW_NUM], TIME_FORMAT) - timedelta(days=1)
                if one_day_deltatime <= created_time:
                    self.assertIn(repository[InsertDataNum.REPOSITORY_TITLE_NUM], pr_list)
                elif one_day_deltatime <= updated_time:
                    self.assertNotIn(repository[InsertDataNum.REPOSITORY_TITLE_NUM], pr_list)


if __name__ == "__main__":
    unittest.main()
