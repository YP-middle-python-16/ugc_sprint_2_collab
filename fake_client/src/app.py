import asyncio
from random import randrange

import aiohttp

import config
import fake_data
from models import EventMessage
from spectator import Spectator


def generate_spectators():
    user_movie = [fake_data.MOVIES[randrange(fake_data.MOVIE_COUNT - 1)] for _ in range(1, fake_data.USER_COUNT)]
    spectators = [Spectator(fake_data.USERS[i], user_movie[i], fake_data.MOVIE_LENGTH[i])
                  for i in range(1, fake_data.USER_COUNT - 1)]
    return spectators


async def one_iteration(session):
    for fake_user in spectators:
        likes_event = None
        comment_event = None
        bookmark_event = None
        film_view_event = fake_user.continue_watch_movie()
        if not (film_view_event is None):
            new_movie_index = randrange(1, fake_data.MOVIE_COUNT - 1)
            # set movie_id for spectator
            fake_user.movie_id = fake_data.MOVIES[new_movie_index]
            # user is starting watching tv
            fake_user.start_watch_movie(fake_data.MOVIE_LENGTH[new_movie_index])
            # user is rating film from 0 to 10
            likes_event = fake_user.rate_film()
            # user is commenting film
            comment_event = fake_user.comment_film()
            # user add film to bookmarks
            bookmark_event = fake_user.bookmark_film()

        key = fake_user.key
        # send movie event
        message = EventMessage(key=key, value=film_view_event.json())
        await session.post(f'http://{config.API_HOST}:{config.API_PORT}/api/v1/event/', json=message.dict())

        # send rating event
        if likes_event:
            message = EventMessage(key=key, value=likes_event.json())
            await session.post(f'http://{config.API_HOST}:{config.API_PORT}/api/v1/likes/', json=message.dict())

        # send comment event
        if comment_event:
            message = EventMessage(key=key, value=comment_event.json())
            await session.post(f'http://{config.API_HOST}:{config.API_PORT}/api/v1/comments/', json=message.dict())

        # send bookmark event
        if bookmark_event:
            message = EventMessage(key=key, value=bookmark_event.json())
            await session.post(f'http://{config.API_HOST}:{config.API_PORT}/api/v1/bookmarks/', json=message.dict())


async def main():
    async with aiohttp.ClientSession() as session:
        while True:
            coros = [one_iteration(session) for _ in range(config.MESSAGES_BATCH_SIZE)]
            await asyncio.gather(*coros)
            await asyncio.sleep(config.SLEEP_PAUSE)


spectators = generate_spectators()
asyncio.run(main())
