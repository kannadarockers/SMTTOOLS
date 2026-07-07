import asyncio

from engine.metadata import TMDBClient


async def main():

    tmdb = TMDBClient()

    movie = await tmdb.search_movie(
        "Interstellar",
        2014
    )

    print(movie)


asyncio.run(main())