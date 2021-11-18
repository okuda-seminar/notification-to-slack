from os.path import join
import unittest
import sqlite3
from datetime import datetime, timedelta

from config.const import DB_ROOT
from src.register_pr import create_table, insert_data


class TestRegisterPr(unittest.TestCase):

    def test_create_table(self):
        """Test of create_table function"""
        db_path = join(DB_ROOT, "test.db")
        create_table(db_path)
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            table = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            # table = [("pull_requests",),("sqlite_sequence",),("repositories",)]
            PULL_REQUESTS_NUM = 0
            REPOSITORIES_NUM = 2
            self.assertEqual(table[PULL_REQUESTS_NUM][0], "pull_requests")
            self.assertEqual(table[REPOSITORIES_NUM][0], "repositories")

    def test_insert_data(self):
        """Test of insert_data function"""
        db_path = join(DB_ROOT, "test.db")
        insert_data(db_path)
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            repositories = cursor.execute("SELECT * FROM repositories").fetchall()
            try:
                self.assertIsNotNone(repositories)
            except TypeError:
                print("pull requests is None")
            pull_requests = cursor.execute("SELECT * FROM pull_requests").fetchall()
            PR_TITLE_NUM = 1
            pr_list = [pr[PR_TITLE_NUM] for pr in pull_requests]
            pr_list = list(set(pr_list))
            if not pr_list:
                self.assertIsNotNone(pull_requests)
            else:
                REPOSITORY_TITLE_NUM = 2
                TIME_CREATED_NUM = 3
                TIME_UPDATED_NUM = 4
                TIME_NOW_NUM = 5
                TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
                for repository in repositories:
                    created_time = datetime.strptime(repository[TIME_CREATED_NUM], TIME_FORMAT)
                    updated_time = datetime.strptime(repository[TIME_UPDATED_NUM], TIME_FORMAT)
                    one_day_deltatime = datetime.strptime(repository[TIME_NOW_NUM], TIME_FORMAT) - timedelta(days=1)
                    if created_time <= one_day_deltatime:
                        if repository[REPOSITORY_TITLE_NUM] in pr_list:
                            pr_list.remove(repository[REPOSITORY_TITLE_NUM])
                    elif updated_time <= one_day_deltatime:
                        self.assertNotIn(repository[REPOSITORY_TITLE_NUM], pr_list)
                self.assertIs(len(pr_list), 0)


if __name__ == "__main__":
    unittest.main()
