from datetime import datetime, timedelta
import sqlite3

import requests

from config import DB_PATH, GITHUB_TOKEN


class RepositoryData:

    def __init__(self, db_name: str) -> None:
        self.db_path = DB_PATH.format(DB_NAME=db_name)

    def insert_repositories(self, data: tuple, cursor: sqlite3.Cursor) -> None:
        """Insert repositories
        Args:
            data(tuple): the data of repository
                (repo_name, pr_id, pr_created_at, pr_updated_at, created_at, updated_at)
            cursor(sqlite3.Cursor): sqlite3's cursor
        """
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


class PullRequestData:

    def __init__(self, db_name: str) -> None:
        self.db_path = DB_PATH.format(DB_NAME=db_name)

    def insert_pull_requests(self, data: tuple, cursor: sqlite3.Cursor) -> None:
        """Insert pull requests
        Args:
            data(tuple): the data of pull request
                (pr_id, pr_title, pr_reviewer, pr_number, pr_url, created_at, updated_at)
            cursor(sqlite3.Cursor): sqlite3's cursor
        """
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

    def delete_pull_requests(self, data: tuple, cursor: sqlite3.Cursor) -> None:
        """Delete pull requests
        Args:
            data(tuple): the data of repository
                (pr_id, reviewer)
            cursor(sqlite3.Cursor): sqlite3's cursor
        """
        cursor.execute(
                "DELETE FROM pull_requests WHERE pr_id = {} AND reviewer NOT IN {}".format(
                    data[0], data[1]
                )
        )


class Github:

    def access_github(self, db_name: str) -> None:
        """Insert data
        """
        pull_request_data = PullRequestData(db_name)
        repository_data = RepositoryData(db_name)

        TOKEN = GITHUB_TOKEN
        headers = {"Authorization": f"token {TOKEN}"}
        repo_url = "https://api.github.com/user/repos"
        repositories = requests.get(repo_url, headers=headers)

        with sqlite3.connect(pull_request_data.db_path) as con:
            cursor = con.cursor()
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
                        try:
                            repository_data.insert_repositories(data, cursor)
                            con.commit()
                        except KeyError:
                            print("An error has occurred in the database processing")
                            con.rollback()

                        created_time = datetime.strptime(pull_request["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                        updated_time = datetime.strptime(pull_request["updated_at"], "%Y-%m-%dT%H:%M:%SZ")

                        if created_time >= datetime.now() - timedelta(days=1):
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

                                try:
                                    pull_request_data.insert_pull_requests(data, cursor)
                                    con.commit()
                                except KeyError:
                                    print("An error has occurred in the database processing")
                                    con.rollback()

                        elif updated_time >= datetime.now() - timedelta(days=1):
                            reviewers = [reviewer["login"] for reviewer in pull_request["requested_reviewers"]]
                            data = (pull_request["node_id"], reviewers)
                            try:
                                pull_request_data.delete_pull_requests(data)
                                con.commit()
                            except KeyError:
                                print("An error has occurred in the database processing")
                                con.rollback()
            except TypeError:
                print("There is no token")


def main():
    Github().access_github('git_slack.db')


if __name__ == "__main__":
    main()
