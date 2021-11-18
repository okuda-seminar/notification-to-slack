from os.path import join
import sqlite3
import requests

import settings
from config.const import DB_ROOT
from datetime import datetime, timedelta


class PrGenerator():
    def __init__(self, repositories, headers):
        """Initialize data structure
        Args:
            repositories: repositories' information
            headers: token
        """
        self.repositories = repositories
        self.headers = headers

    def __iter__(self):
        """Iterate repositories
        """
        for repository in self.repositories.json():
            owner = repository["owner"]["login"]
            repo = repository["name"]
            pull_request_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
            pull_requests = requests.get(pull_request_url, headers=self.headers)
            for pull_request in pull_requests.json():
                yield repository, pull_request


def create_table(db_path: str) -> None:
    """create_table
    Args:
        db_path (str): database path
    """
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS pull_requests( \
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                pr_id TEXT,\
                pr_title TEXT,\
                pr_reviewer TEXT,\
                pr_number INT,\
                pr_url TEXT, \
                created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')),\
                updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\'))\
            )"
        )
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS repositories(\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                repo_name TEXT,\
                pr_id TEXT,\
                pr_created_at TEXT NOT NULL DEFAULT DATETIME,\
                pr_updated_at TEXT NOT NULL DEFAULT DATETIME,\
                created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')),\
                updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\'))\
            )"
        )


def insert_data(db_path: str):
    """insert data
    Args:
        db_path (str): database path
    """
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        token = settings.GITHUB_TOKEN
        TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        headers = {"Authorization": f"token {token}"}
        repo_url = "https://api.github.com/user/repos"
        repositories = requests.get(repo_url, headers=headers)
        try:
            for repository, pull_request in PrGenerator(repositories, headers):
                cursor.execute(
                    "INSERT INTO repositories(\
                        repo_name, pr_id, pr_created_at,\
                        pr_updated_at, created_at, updated_at\
                    )\
                    VALUES(?, ?, ?, ?, ?, ?)", (
                        repository["full_name"],
                        pull_request["node_id"],
                        datetime.strptime(pull_request["created_at"], TIME_FORMAT),
                        datetime.strptime(pull_request["updated_at"], TIME_FORMAT),
                        datetime.now(),
                        datetime.now()
                    )
                )
                created_time = datetime.strptime(pull_request["created_at"], TIME_FORMAT)
                updated_time = datetime.strptime(pull_request["updated_at"], TIME_FORMAT)
                if created_time <= datetime.now() - timedelta(days=1):
                    for reviewer in pull_request["requested_reviewers"]:
                        cursor.execute(
                            "INSERT INTO pull_requests(\
                                pr_id, pr_title, pr_reviewer,\
                                pr_number, pr_url, created_at, updated_at\
                            )\
                            VALUES(?, ?, ?, ?, ?, ?, ?)", (
                                pull_request["node_id"],
                                pull_request["title"],
                                reviewer["login"],
                                pull_request["number"],
                                pull_request["url"],
                                datetime.now(),
                                datetime.now()
                            )
                        )
                elif updated_time <= datetime.now() - timedelta(days=1):
                    reviewers = [reviewer["login"] for reviewer in pull_request["requested_reviewers"]]
                    cursor.execute("DELETE FROM pull_requests WHERE pr_id = {} AND reviewer NOT IN {}".format(
                        pull_request["ode_id"], reviewers))
            con.commit()
        except TypeError:
            print("There is no token")


if __name__ == "__main__":
    db_path = join(DB_ROOT, "git-slack.db")
    create_table(db_path)
    insert_data(db_path)