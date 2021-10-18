import unittest
import sqlite3

from scripts.register_pr import create_table, insert_data

class TestRegisterPr(unittest.TestCase):
    def test_create_table(self):
        path = "./test.db"
        create_table(path)
        con = sqlite3.connect(path)
        cursor = con.cursor()
        self.assertEqual(cursor.execute("""SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='pull_requests';""").fetchall()[0][0],1)
        self.assertEqual(cursor.execute("""SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='repositories';""").fetchall()[0][0],1)
        cursor.close()
        con.close()
    def test_insert_data(self):
        path = "./test.db"
        insert_data(path)
        con = sqlite3.connect(path)
        cursor = con.cursor()
        if cursor.execute('SELECT * FROM pull_requests').fetchone() != None:
            self.assertEqual(len(cursor.execute('SELECT * FROM pull_requests').fetchone()),8)
        self.assertEqual(len(cursor.execute('SELECT * FROM repositories').fetchone()),5)
        cursor.close()
        con.close()



if __name__ == '__main__':
    unittest.main()