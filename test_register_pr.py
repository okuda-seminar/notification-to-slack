import unittest
import sqlite3

from scripts.register_pr import create_table, insert_data


class TestRegisterPr(unittest.TestCase):
    """test of scripts/register_pr.py"""
    def test_create_table(self):
        """test of create_table function"""
        # setting test database path
        path = "./test.db"
        # call create_table function
        create_table(path)
        con = sqlite3.connect(path)
        cursor = con.cursor()
        # sql context (why separate ? <- sql context is too long)
        sql_pull = """SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='pull_requests';"""
        sql_repo = """SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='repositories';"""
        # presence or absence of creating table by create_table function
        self.assertEqual(cursor.execute(sql_pull).fetchall()[0][0], 1)
        self.assertEqual(cursor.execute(sql_repo).fetchall()[0][0], 1)
        cursor.close()
        con.close()

    def test_insert_data(self):
        """test of insert_data function"""
        # setting test database path
        path = "./test.db"
        # call insert_data function
        insert_data(path)
        con = sqlite3.connect(path)
        cursor = con.cursor()
        # conditional branch of presence or absence on pull_requests table
        if cursor.execute('SELECT * FROM pull_requests').fetchone() is None:
            # absence of pull_requests table
            self.assertIsNone(cursor.execute('SELECT * FROM pull_requests').fetchone())
        else:
            # presence of pull_requests table
            self.assertEqual(len(cursor.execute('SELECT * FROM pull_requests').fetchone()), 8)
        # check of insert data in repositories table
        self.assertEqual(len(cursor.execute('SELECT * FROM repositories').fetchone()), 5)
        cursor.close()
        con.close()


if __name__ == '__main__':
    unittest.main()
