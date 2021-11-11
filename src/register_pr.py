from os.path import join
import sqlite3
import requests

from config import DB_ROOT
from datetime import datetime, timedelta


def create_table(db_path: str) -> None:
    """create_table
    Args:
        db_path (str): database path
    """
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS pull_requests( \
                        id INTEGER PRIMARY KEY AUTOINCREMENT,\
                        pr_id TEXT,\
                        pr_title TEXT,\
                        pr_reviewer TEXT,\
                        pr_number INT,\
                        pr_url TEXT, \
                        created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')),\
                        updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\'))\
                        )")
        cursor.execute("CREATE TABLE IF NOT EXISTS repositories(\
                        id INTEGER PRIMARY KEY AUTOINCREMENT,\
                        repo_name TEXT,\
                        pr_id TEXT,\
                        pr_created_at TEXT NOT NULL DEFAULT DATETIME,\
                        pr_updated_at TEXT NOT NULL DEFAULT DATETIME,\
                        created_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\')),\
                        updated_at TEXT NOT NULL DEFAULT (DATETIME(\'now\', \'localtime\'))\
                        )")


def insert_data(db_path: str):
    """insert data
    Args:
        db_path (str): database path
    """
    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        token = "token"
        headers = {"Authorization": f"token {token}"}
        repo_url = "https://api.github.com/user/repos"
        repositories = requests.get(repo_url, headers=headers)
        try:
            for repository in repositories.json():
                owner = repository["owner"]["login"]
                repo = repository["name"]

                pull_request_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
                pull_requests = requests.get(pull_request_url, headers=headers)
                for pull_request in pull_requests.json():
                    cursor.execute("INSERT INTO repositories(repo_name, pr_id, pr_created_at, pr_updated_at,\
                                    created_at, updated_at)\
                                    VALUES(?, ?, ?, ?, ?, ?)", (
                                        repository["full_name"],
                                        pull_request["node_id"],
                                        datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
                                        datetime.strptime(pull_request["updated_at"], "%Y-%m-%dT%H:%M:%SZ"),
                                        datetime.now(),
                                        datetime.now()
                                    ))
                    created_time = datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    updated_time = datetime.strptime(pull_request["updated_at"], "%Y-%m-%dT%H:%M:%SZ")
                    if created_time <= datetime.now() - timedelta(days=1):
                        for reviewer in pull_request["requested_reviewers"]:
                            cursor.execute("INSERT INTO pull_requests(pr_id, pr_title, pr_reviewer,\
                                            pr_number, pr_url, created_at, updated_at)\
                                            VALUES(?, ?, ?, ?, ?, ?, ?)", (
                                                pull_request["node_id"],
                                                pull_request["title"],
                                                reviewer["login"],
                                                pull_request["number"],
                                                pull_request["url"],
                                                datetime.now(),
                                                datetime.now()
                                            ))
                    elif updated_time <= datetime.now() - timedelta(days=1):
                        reviewers = [reviewer["login"] for reviewer in pull_request["requested_reviewers"]]
                        cursor.execute("DELETE FROM pull_requests WHERE pr_id = {} AND reviewer NOT IN {}".format(
                            pull_request["node_id"], reviewers))
            con.commit()
        except TypeError:
            print("There is no token")


if __name__ == "__main__":
    db_path = join(DB_ROOT, "git-slack.db")
    create_table(db_path)
    insert_data(db_path)
