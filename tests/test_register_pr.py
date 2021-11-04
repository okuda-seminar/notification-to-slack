from os.path import join
import unittest
import sqlite3
from datetime import datetime, timedelta

from config.const import DB_ROOT
from src.register_pr import create_table, insert_data


class TestRegisterPr(unittest.TestCase):

    def test_create_table(self):
        """test create_table
        check arbitrary database existed tables
        """
        # setting test database path
        db_path = join(DB_ROOT, "test.db")
        # call create_table function
        create_table(db_path)
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            # get table in db
            # [("pull_requests",),("sqlite_sequence",),("repositories",)]
            table = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            # whether table[0] is pull_requests
            self.assertEqual(table[0][0], "pull_requests")
            # wheter table[2] is repositories
            self.assertEqual(table[2][0], "repositories")

    def test_insert_data(self):
        """test of insert_data function"""
        # setting test database path
        db_path = join(DB_ROOT, "test.db")
        # call create_table function
        insert_data(db_path)
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            # get one record in repositories table
            repositories = cursor.execute("SELECT * FROM repositories").fetchall()
            # if there are some pull request in repositories
            try:
                self.assertIsNotNone(repositories)
            except TypeError:
                print("pull requests is None")
            pull_requests = cursor.execute("SELECT * FROM pull_requests").fetchall()
            pr_list = [pr[1] for pr in pull_requests]
            if not pr_list:
                self.assertIsNotNone(pull_requests)
            else:
                for repo in repositories:
                    created_time = repo[3]
                    if created_time <= datetime.now() - timedelta(days=1):
                        self.assertRegexpMatches(repo[2], pr_list)
                    else:
                        self.assertNotRegexpMatches(repo[2], pr_list)


if __name__ == "__main__":
    unittest.main()
