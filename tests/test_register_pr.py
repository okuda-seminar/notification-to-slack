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
            pull_requests_num = 0
            repositories_num = 2
            self.assertEqual(table[pull_requests_num][0], "pull_requests")
            self.assertEqual(table[repositories_num][0], "repositories")

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
            pr_title_num = 1
            pr_list = [pr[pr_title_num] for pr in pull_requests]
            pr_list = list(set(pr_list))
            if not pr_list:
                self.assertIsNotNone(pull_requests)
            else:
                repository_title_num = 2
                time_create_num = 3
                time_update_num = 4
                time_now_num = 5
                for repository in repositories:
                    created_time = datetime.strptime(repository[time_create_num], "%Y-%m-%d %H:%M:%S")
                    updated_time = datetime.strptime(repository[time_update_num], "%Y-%m-%d %H:%M:%S")
                    one_day_deltatime = datetime.strptime(repository[time_now_num], "%Y-%m-%d %H:%M:%S.%f") - timedelta(days=1)
                    if created_time <= one_day_deltatime:
                        if repository[repository_title_num] in pr_list:
                            pr_list.remove(repository[repository_title_num])
                    elif updated_time <= one_day_deltatime:
                        self.assertNotIn(repository[repository_title_num], pr_list)
                self.assertIs(len(pr_list), 0)


if __name__ == "__main__":
    unittest.main()
