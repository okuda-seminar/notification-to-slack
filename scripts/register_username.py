from config import DB_ROOT
import sqlite3
from datetime import datetime
import logging
import argparse

def insert_username(db, new_data):
  with sqlite3.connect(db) as con:
    cursor = con.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usernames(\
                    id INTEGER PRIMARY KEY AUTOINCREMENT,\
                    slack_user_id TEXT,\
                    github_name TEXT,\
                    created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')),\
                    updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')))')

    cursor.execute('SELECT * FROM usernames WHERE (slack_user_id=? AND github_name=?)', (new_data))
    entry = cursor.fetchone()

    if entry is None:
      cursor.execute('INSERT INTO usernames(slack_user_id, github_name, created_at, updated_at) VALUES (?,?,?,?)', (new_data[0], new_data[1], datetime.now(), datetime.now()))
      con.commit()
      con.close()
      logger.info('The username on Github has been registered in the database.')
    else:
      con.close()
      logger.warning('The username on Github is already registered in the database.')


if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  parser = argparse.ArgumentParser()
  parser.add_argument("-param1", help="parameter1 discription")
  parser.add_argument("-param2", help="parameter2 discription")
  args = parser.parse_args()
  new_data = (args.param1, args.param2)
  logger = logging.getLogger(__name__)
  db_name = "git_slack.db"
  db = f'{DB_ROOT}/{db_name}'
  insert_username(db, new_data)