import argparse
import logging
import sqlite3

import write

from config import DB_ROOT


def read_pr(db_path: str, slack_user_id: str, repository_name: str) -> None:
  """return PR titles

  Args:
    db_path(str): path to the git_slack.db
    slack_user_id(str): slack user id
    repository_name(str): repository name
  """
  with sqlite3.connect(db_path) as con:
    cursor = con.cursor()
    cursor.execute('SELECT github_name FROM usernames WHERE slack_user_id = ?', slack_user_id)
    github_user_entry = cursor.fetchone()

    if not github_user_entry:
      msg = 'Unregistered Github username'
      log_level = "warning"
      con.close()

    cursor.execute('SELECT pr_title, pr_number, pr_url FROM pull_requests WHERE pr_reviewer = ? AND repo_name = ?', (github_user_entry, repository_name))
    pr_titles = cursor.fetchall()

    if not pr_titles:
      msg = 'No Pull Request to review'
      log_level = "info"
      con.close()

    msg = pr_titles
    log_level = "info"

    writer = write.MultipleWriter()
    writer.write(msg, log_level)
  
    con.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-param1", type=str, default=None, help="slack_user")
  parser.add_argument("-param2", type=str, default=None, help="repository")
  slack_user_id, repository_name = parser.parse_args()[:2]

  db_path = "{DB_ROOT}/{DB_NAME}".format(DB_ROOT=DB_ROOT, DB_NAME="git_slack.db")
  log_path = "{DB_ROOT}/{LOG_NAME}".format(DB_ROOT=DB_ROOT, LOG_NAME="logger.log")

  logging.basicConfig(filename=log_path, level=logging.INFO)
  logger = logging.getLogger(__name__)

  read_pr(db_path, slack_user_id, repository_name)