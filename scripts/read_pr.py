import argparse
import sqlite3

from write import MultipleWriter

from config import DB_PATH


def read_pr(db_path: str, slack_user_id: str, repository_name: str) -> None:
    """Return PR titles
    Args:
      db_path(str): path to the git_slack.db
      slack_user_id(str): slack user id
      repository_name(str): repository name
    """
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute(
            'SELECT github_name FROM usernames WHERE slack_user_id = ?', (
                slack_user_id
            )
        )
        github_user_entry = cursor.fetchone()

        if not github_user_entry:
            msg = 'Unregistered Github username'
            log_level = "warning"

        cursor.execute(
            'SELECT pr_title, pr_number, pr_url\
            FROM pull_requests\
            INNER JOIN repositories ON repositories.pr_id = pull_requests.pr_id\
            WHERE pr_reviewer = ? AND repo_name = ?', (
                github_user_entry, repository_name
            )
        )
        pr_titles = cursor.fetchall()

        if len(pr_titles) == 0:
            msg = 'No Pull Request to review'
            log_level = "info"

        if not msg:
            msg = pr_titles
            log_level = "info"

        writer.write(msg, log_level)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-param1", type=str, default=None, help="slack_user")
    parser.add_argument("-param2", type=str, default=None, help="repository")
    args = parser.parse_args()
    slack_user_id, repository_name = args.param1, args.param2

    db_path = DB_PATH.format(DB_NAME="git-slack.db")

    writer = MultipleWriter()

    read_pr(db_path, slack_user_id, repository_name)
