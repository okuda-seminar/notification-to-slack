import argparse
import logging
import sqlite3

from datetime import datetime

from config import DB_ROOT


def insert_username(db: str, new_data: tuple):
  """insert the user's information into database

  Args:
    db(str): pass to the git_slack.db
    new_data(tuple): user information, (slack_user_id, github_username)
  """
  with sqlite3.connect(db) as con:
    cursor = con.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usernames(\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    slack_user_id TEXT,\
                    github_name TEXT,\
                    created_at TEXT NOT NULL DEFAULT\
                    (DATETIME(\'now\', \'localtime\')),\
                    updated_at TEXT NOT NULL DEFAULT\
                    (DATETIME(\'now\', \'localtime\')))')

    cursor.execute('SELECT * FROM usernames WHERE\
                    (slack_user_id=? AND github_name=?)', (new_data))
    entry = cursor.fetchone()

    if entry is None:
      cursor.execute('INSERT INTO usernames(slack_user_id, github_name, created_at, updated_at)\
                      VALUES (?,?,?,?)', (new_data[0], new_data[1], datetime.now(), datetime.now()))
      con.commit()
      con.close()
      message = 'The username on Github has been registered in the database.'
      logger.info(message)
    else:
      con.close()
      message = 'The username on Github is already registered in the database.'
      logger.warning(message)
    print(message)


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-param1", type=str, default=None, help="slack_user")
  parser.add_argument("-param2", type=str, default=None, help="github_user")
  args = parser.parse_args()
  new_data = (args.param1, args.param2)
  DB_NAME = "git_slack.db"
  db = f'{DB_ROOT}/{DB_NAME}'
  LOG_NAME = "loger.log"
  log = f'{DB_ROOT}/{LOG_NAME}'
  logging.basicConfig(filename=log, level=logging.INFO)
  logger = logging.getLogger(__name__)
  insert_username(db, new_data)