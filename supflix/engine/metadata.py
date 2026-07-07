import os
import httpx
from dotenv import load_dotenv

load_dotenv()


class TMDBClient:

    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE = "https://image.tmdb.org/t/p/original"

    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")

    async def search_movie(self, title, year=None):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/search/movie",
                params={
                    "api_key": self.api_key,
                    "query": title,
                    "year": year
                }
            )

            return response.json()

    async def search_tv(self, title):

        async with httpx.AsyncClient() as client:

            response = await client.get(
                f"{self.BASE_URL}/search/tv",
                params={
                    "api_key": self.api_key,
                    "query": title
                }
            )

            return response.json()
            
            
from dataclasses import dataclass
from typing import Optional

@dataclass
class Metadata:
    tmdb_id: int
    title: str
    overview: str
    poster: str
    backdrop: str
    rating: float
    runtime: Optional[int]
    genres: list[str]
    release_date: str