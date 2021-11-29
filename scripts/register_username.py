import argparse
import sqlite3

from write import MultipleWriter

from config import DB_PATH


def insert_username(db_path : str, new_data: tuple) -> None:
    """Insert the user's information into database

    Args:
        db_path(str): path to the git_slack.db
        new_data(tuple): user information, (slack_user_id, github_username)
    """
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS usernames(\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            slack_user_id TEXT,\
            github_name TEXT,\
            created_at TEXT NOT NULL DEFAULT\
            (DATETIME(\'now\', \'utc\')),\
            updated_at TEXT NOT NULL DEFAULT\
            (DATETIME(\'now\', \'utc\')))'
        )

        cursor.execute(
            'SELECT * FROM usernames WHERE\
            (slack_user_id=? AND github_name=?)',
            (new_data)
        )

        entry = cursor.fetchone()

        if entry is None:
            cursor.execute(
                'INSERT INTO usernames(slack_user_id, github_name)\
                VALUES (?,?)',
                (new_data[0], new_data[1])
            )
            con.commit()
            msg = 'The username on Github has been registered in the database.'
            log_level = "info"
        else:
            msg = 'The username on Github is already registered in the database.'
            log_level = "warning"

        writer.write(msg, log_level)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-param1", type=str, default=None, help="slack_user")
    parser.add_argument("-param2", type=str, default=None, help="github_user")
    args = parser.parse_args()
    new_data = (args.param1, args.param2)

    db_path = DB_PATH.format(DB_NAME="git-slack.db")
    writer = MultipleWriter()

    insert_username(db_path, new_data)