import uuid
from random import randrange
from datetime import datetime
import time

from rich.progress import Progress

import config
from benchmarks import BATCH_SEQUENCE
from model import MovieViewEvent, MovieSelection
from visualization import show_result


class BenchMark:
    def __init__(self):
        self.tasks = {}
        self.progress = Progress()

        self.users = [uuid.uuid4() for i in range(1, config.USER_COUNT)]
        self.movies = [uuid.uuid4() for i in range(1, config.MOVIE_COUNT)]
        self.user_movie = [self.movies[randrange(config.MOVIE_COUNT - 1)] for i in range(1, config.USER_COUNT)]
        self.movie_lengths = [randrange(config.MOVIE_MAX_LEN) for i in range(1, config.USER_COUNT)]

    def benchmark_service_single_insert(self, service):
        time_now = datetime.now()
        time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")

        counter = 0

        for user_counter in range(1, config.USER_COUNT - 1):
            user_current_movie_id = self.user_movie[user_counter]
            for tick in range(1, self.movie_lengths[user_counter]):
                data = MovieViewEvent(
                    movie_id=str(user_current_movie_id),
                    user_id=str(self.users[user_counter]),
                    event_time=time_now,
                    view_run_time=tick
                )
                counter = counter + 1
                service.insert(data=data)

        return counter

    def benchmark_service_batch_insert(self, service):
        time_now = datetime.now()
        time_now = time_now.strftime("%Y-%m-%d %H:%M:%S")
        data = []

        counter = 0

        for user_counter in range(1, config.USER_COUNT - 1):
            user_current_movie_id = self.user_movie[user_counter]
            for tick in range(1, self.movie_lengths[user_counter]):
                row = MovieViewEvent(
                    movie_id=str(user_current_movie_id),
                    user_id=str(self.users[user_counter]),
                    event_time=time_now,
                    view_run_time=tick
                )
                counter = counter + 1
                data.append(row)

        service.insert_batch(data=data)

        return counter

    def benchmark_service_select(self, service):
        counter = 0

        for user_counter in range(1, config.USER_COUNT - 1):
            user_current_movie_id = self.user_movie[user_counter]
            movie = MovieSelection(
                movie_id=str(user_current_movie_id),
                user_id=str(self.users[user_counter])
            )
            counter = counter + 1
            service.select(data=movie)

        return counter

    def benchmark_service(self, storage, mode):
        service = BATCH_SEQUENCE[storage]['client']

        # insert
        counter_insert = 0
        timer_insert = 0
        if BATCH_SEQUENCE[storage]['use_insert']:
            t0 = time.time()
            self.tasks[storage + ":insert"] = self.progress.add_task(f"[cyan]{storage} insert",
                                                                     total=config.BATCHES - 1)
            current_count = 0
            for i in range(1, config.BATCHES):
                if mode == "single":
                    current_count = self.benchmark_service_single_insert(service=service)
                if mode == "batch":
                    current_count = self.benchmark_service_batch_insert(service=service)

                counter_insert = counter_insert + current_count
                self.progress.update(self.tasks[storage + ":insert"], advance=1)

            timer_insert = time.time() - t0

        # select
        counter_select = 0
        timer_select = 0
        if BATCH_SEQUENCE[storage]['use_select']:
            t0 = time.time()
            self.tasks[storage + ":select"] = self.progress.add_task(f"[cyan]{storage} select",
                                                                     total=config.BATCHES - 1)
            for i in range(1, config.BATCHES):
                current_count = self.benchmark_service_select(service=service)

                counter_select = counter_select + current_count
                self.progress.update(self.tasks[storage + ":select"], advance=1)

            timer_select = time.time() - t0

        row_stat = {
            'storage': storage,
            'mode': mode,
            'runtime_insert': timer_insert,
            'runtime_select': timer_select,
            'counter_insert': counter_insert,
            'counter_select': counter_select
        }

        return row_stat

    def run(self):
        statistics = []
        with Progress() as progress:
            self.progress = progress
            for item in BATCH_SEQUENCE:
                if BATCH_SEQUENCE[item]['use']:
                    mode = BATCH_SEQUENCE[item]['mode']
                    storage_name = BATCH_SEQUENCE[item]['storage']

                    row_stat = self.benchmark_service(item, mode)
                    statistics.append(row_stat)

        return statistics


if __name__ == '__main__':
    app = BenchMark()
    statistics = app.run()
    show_result(statistics)
