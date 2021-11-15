from datetime import datetime
import sqlite3
import time
import unittest
from unittest.mock import PropertyMock, MagicMock, patch

import hydra
from omegaconf import DictConfig, OmegaConf
import requests

from config import DB_PATH
from src.register_pr import PullRequest 


class Timer(object):
    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        print('  => elapsed time: %f s' % self.secs)


class TestDatabase(unittest.TestCase):
    def create_table(self, db_path: str) -> None:
        """Create repositories table
        Args:
            db_path(str): path to database
        """
        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
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
            con.commit()


    def test_insert_pull_request(self, data_num: int, db_name: str) -> None:
        """Test the insertion of the pull requests
        Args:
            data_num(int): number of data to insert
            db_name(str): name of database
        """
        result_mock = MagicMock()
        type(result_mock).lastrowid = PropertyMock(return_value=1)

        cur_mock = MagicMock()
        cur_mock.execute.return_value = result_mock

        conn_mock = MagicMock()
        conn_mock.cursor.return_value = cur_mock

        with patch("sqlite3.connect", return_value=conn_mock):
            pull_request = PullRequest(db_name)
            for i in range(data_num):
                data = (
                    "repo_name{}".format(i),
                    "pr_id{}".format(i),
                    datetime.now(),
                    datetime.now(),
                    datetime.now(),
                    datetime.now()
                )

                pull_request.insert_repositories(data)


@hydra.main(config_name="config")
def benchmark_db(cfg: DictConfig) -> None:
    """Benchmark test the performance of the database
    """
    benchmark_pull_request = TestDatabase()

    db_name = "dummy.db"
    db_path = DB_PATH.format(DB_NAME=db_name)
    benchmark_pull_request.create_table(db_path)

    INIT_NUM = cfg.benchmark.init
    TOTAL_NUM = cfg.benchmark.total
    INTERVAL_NUM = cfg.benchmark.interval

    for i in range(INIT_NUM, TOTAL_NUM, INTERVAL_NUM):
        with Timer() as t:
            benchmark_pull_request.test_insert_pull_request(data_num=i, db_name=db_name)

    with sqlite3.connect(db_path) as con:
        cursor = con.cursor()
        cursor.execute("""DROP TABLE repositories""")
        con.commit()


if __name__ == "__main__":
    print('Doing')
    benchmark_db()
