from datetime import datetime
from os import makedirs
import sqlite3
import time
import unittest
from unittest.mock import PropertyMock, MagicMock, patch

import plotly.graph_objects as go
import numpy as np
import hydra
from omegaconf import DictConfig, OmegaConf
import requests

from config import DB_PATH, FIG_PATH, FIG_ROOT
from src.register_pr import PullRequest 


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

class Visualizer:

    @staticmethod
    def visualize(x: np.ndarray, y: np.ndarray, title: str = "benchmark test") -> None:
        """Save figure.
        Args:
            x(np.ndarray): data points
            y(np.ndarray): elapsed time
            title(str): figure title
        """
        times_average = np.average(y, axis=0)
        times_var = np.var(y, axis=0)
        
        fig = go.Figure(
                data=go.Scatter(
                    x=x,
                    y=times_average,
                    name=title,
                    error_y=dict(
                        type="data",
                        array=times_var, 
                        visible=True
                    )
                )
            )
        fig.update_xaxes(title='number of data')
        fig.update_yaxes(title='elapsed time')
        fig.update_layout(title=title)

        makedirs(FIG_ROOT, exist_ok=True)
        fig_path = FIG_PATH.format(FIG_NAME=title)
        fig.write_image(fig_path)


@hydra.main(config_name="config")
def benchmark_db(cfg: DictConfig) -> None:
    """Benchmark test the performance of the database
    """
    benchmark_pull_request = TestDatabase()

    db_name = "dummy.db"
    db_path = DB_PATH.format(DB_NAME=db_name)

    INIT_NUM = cfg.benchmark.init
    TOTAL_NUM = cfg.benchmark.total
    INTERVAL_NUM = cfg.benchmark.interval
    EXPERIMENT_NUM = cfg.benchmark.experiment

    for i in range(EXPERIMENT_NUM):
        cur_result_times = np.array([])
        benchmark_pull_request.create_table(db_path)
        for num in range(INIT_NUM, TOTAL_NUM, INTERVAL_NUM):
            start_time = time.time()
            benchmark_pull_request.test_insert_pull_request(data_num=num, db_name=db_name)
            end_time = time.time()

            elapsed_time = end_time - start_time
            print('  => elapsed time: %f s' % elapsed_time)

            cur_result_times = np.append(cur_result_times, elapsed_time)
            cur_result_times.reshape(1, -1)

        with sqlite3.connect(db_path) as con:
            cursor = con.cursor()
            cursor.execute("""DROP TABLE repositories""")
            con.commit()

        if i == 0:
            result_times = cur_result_times
        else:
            result_times = np.vstack((result_times, cur_result_times))

    x = np.arange(INIT_NUM, TOTAL_NUM, INTERVAL_NUM)
    Visualizer.visualize(x, result_times)


if __name__ == "__main__":
    print('Doing')
    benchmark_db()
