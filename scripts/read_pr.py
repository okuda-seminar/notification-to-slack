import argparse
import logging
import sqlite3

from config import DB_ROOT


def read_pr(db: str, slack_user_id: str, repo: str):
  """return pr titles

  Args:
    db(str): pass to the git_slack.db
    slack_user_id(str): slack user id
    repo(str): repository name
  """
  with sqlite3.connect(db) as con:
    cursor = con.cursor()
    cursor.execute('SELECT github_name FROM usernames WHERE slack_user_id = ?', slack_user_id)
    github_user_entry = cursor.fetchone()
    if not github_user_entry:
      logger.warning('Unregistered Github username')
      con.close()

    cursor.execute('SELECT pr_title, pr_number, pr_url FROM pull_requests WHERE pr_reviewer = ? AND repo_name = ?', (github_user_entry, repo))
    pr_titles = cursor.fetchall()

    if not pr_titles:
      logger.info('No Pull Request to review')
      con.close()
      
    logger.info(pr_titles)
    con.close()


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("-param1", type=str, default=None, help="slack_user")
  parser.add_argument("-param2", type=str, default=None, help="repository")
  args = parser.parse_args()
  slack_user_id = args[0]
  repo = args[1]
  DB_NAME = "git_slack.db"
  db = f'{DB_ROOT}/{DB_NAME}'
  logging.basicConfig(level=logging.INFO)
  logger = logging.getLogger(__name__)
  read_pr(db, slack_user_id, repo)