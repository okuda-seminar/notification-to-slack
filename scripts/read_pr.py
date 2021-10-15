import sqlite3
import sys
import logging
from config import DB_ROOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

args = sys.stdin.readline().rstrip()
slack_user_id = args[0]
repo = args[1]

db_name = "git_slack.db"
db = f'{DB_ROOT}/{db_name}'
con = sqlite3.connect(db)
cursor = con.cursor()
cursor.execute('SELECT github_name FROM usernames WHERE slack_user_id = ?', slack_user_id)
github_user_entry = cursor.fetchone()

if not github_user_entry:
  logger.warning('Unregistered Github username')
  con.close()

cursor.execute('SELECT pr_title, pr_number, pr_url FROM pull_requests WHERE pr_reviewer = ? AND repo_name = ?', (github_user_entry, repo))
pr_titles = cursor.fetchall()
print(pr_titles)

if not pr_titles:
  logger.info('No Pull Request to review')
  con.close()
  
logger.info(pr_titles)
con.close()