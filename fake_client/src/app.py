import asyncio
import aiohttp
from random import randrange

from spectator import Spectator
from models import EventMessage
import config
import fake_data


def generate_spectators():
    user_movie = [fake_data.MOVIES[randrange(fake_data.MOVIE_COUNT - 1)] for _ in range(1, fake_data.USER_COUNT)]
    spectators = [
        Spectator(fake_data.USERS[i], user_movie[i], fake_data.MOVIE_LENGTH[i]) for i in range(1, fake_data.USER_COUNT - 1)
    ]
    return spectators


async def one_iteration(session):
    for fake_user in spectators:
        film_view_event = fake_user.continue_watch_movie()
        if not (film_view_event is None):
            new_movie_index = randrange(1, fake_data.MOVIE_COUNT - 1)
            fake_user.start_watch_movie(fake_data.MOVIES[new_movie_index], fake_data.MOVIE_LENGTH[new_movie_index])

        key = fake_user.key
        message = EventMessage(key=key, value=film_view_event.json())

        await session.post(f"http://{config.API_HOST}:{config.API_PORT}/api/v1/event/", json=message.dict())


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            coros = [one_iteration(session) for _ in range(config.MESSAGES_BATCH_SIZE)]
            await asyncio.gather(*coros)
            await asyncio.sleep(config.SLEEP_PAUSE)


spectators = generate_spectators()
asyncio.run(main())
