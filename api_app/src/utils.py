import asyncio
import logging
from functools import wraps

from fastapi.logger import logger
from fastapi import Request


def backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)
    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            n = 0
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    sleep_time = start_sleep_time * factor ** n
                    logger.info(f'sleep_time: {sleep_time}, border_sleep_time: {border_sleep_time}')
                    if sleep_time >= border_sleep_time:
                        raise e
                    await asyncio.sleep(sleep_time)
                    n += 1

        return inner

    return func_wrapper


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = Request.headers.get('X-Request-Id')
        return True
