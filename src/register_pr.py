from datetime import datetime, timedelta
from os.path import join
import sqlite3

import requests

from config import DB_PATH


class PullRequest:
    def __init__(self, db_name: str) -> None:
        self.db_path = DB_PATH.format(DB_NAME=db_name)

    def insert_repositories(self, data: tuple) -> None:
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(
                    "INSERT INTO repositories(\
                            repo_name,\
                            pr_id,\
                            pr_created_at,\
                            pr_updated_at,\
                            created_at,\
                            updated_at\
                    )\
                VALUES(?, ?, ?, ?, ?, ?)", data
            )
            con.commit()

    def insert_pull_requests(self, data: tuple) -> None:
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(
                    "INSERT INTO pull_requests(\
                            pr_id,\
                            pr_title,\
                            pr_reviewer,\
                            pr_number,\
                            pr_url,\
                            created_at,\
                            updated_at\
                    )\
                VALUES(?, ?, ?, ?, ?, ?, ?)", data
            )
            con.commit()

    def delete_pull_requests(self, data: tuple) -> None:
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(
                    "DELETE FROM pull_requests WHERE pr_id = {} AND reviewer NOT IN {}".format(
                    data[0], data[1]
                    )
            )
            con.commit()

    def insert_data(self) -> None:
        """Insert data
        """
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
                    data = (
                        repository["full_name"],
                        pull_request["node_id"],
                        datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
                        datetime.strptime(pull_request["updated_at"], "%Y-%m-%dT%H:%M:%SZ"),
                        datetime.now(),
                        datetime.now()
                    )
                    self.insert_repositories(data)

                    created_time = datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    updated_time = datetime.strptime(pull_request["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

                    if created_time <= datetime.now() - timedelta(days=1):
                        for reviewer in pull_request["requested_reviewers"]:
                            data = (
                                pull_request["node_id"],
                                pull_request["title"],
                                reviewer["login"],
                                pull_request["number"],
                                pull_request["url"],
                                datetime.now(),
                                datetime.now()
                            )

                            self.insert_pull_requests(data)

                    elif updated_time <= datetime.now() - timedelta(days=1):
                        reviewers = [reviewer["login"] for reviewer in pull_request["requested_reviewers"]]
                        data = (pull_request["node_id"], reviewers)
                        self.delete_pull_requests(data)
        except TypeError:
            print("There is no token")

def main():
    pull_request = PullRequest('git_slack.db')
    pull_request.access_github()

if __name__ == "__main__":
    main()
