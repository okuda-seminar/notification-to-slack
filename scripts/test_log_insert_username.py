import unittest

from config import DB_PATH
from register_username import insert_username


class TestLogInsertUserName(unittest.TestCase):
    def test_info_logging_insert_username(self) -> None:
        """Verify that the info log is being output correctly
        """
        db_path = DB_PATH.format(DB_NAME="git-slack.db")
        new_data = ('test_new', 'test_new')

        with self.assertLogs() as captured:
            insert_username(db_path, new_data)

        self.assertEqual(len(captured.records), 1) # check that there is only one log message
        self.assertEqual(captured.records[0].getMessage(), "The username on Github has been registered in the database.")


    def test_warning_logging_insert_username(self) -> None:
        """Verify that the warning log is being output correctly
        """
        db_path = DB_PATH.format(DB_NAME="git-slack.db")
        existed_data = ('test_existed', 'test_existed')

        with self.assertLogs() as captured:
            insert_username(db_path, existed_data)

        self.assertEqual(len(captured.records), 1) # check that there is only one log message
        self.assertEqual(captured.records[0].getMessage(), "The username on Github is already registered in the database.")


if __name__ == "__main__":
    unittest.main()