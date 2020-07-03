"""
Podcast searching via iTunes.
See https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html  # noqa: E501  pylint: disable=line-too-long
for iTunes API Description.
"""

from dataclasses import dataclass
from typing import List, Optional
from podsearch import http

BASE_URL = "https://itunes.apple.com"
SEARCH_URL = f"{BASE_URL}/search"
GET_URL = f"{BASE_URL}/lookup"
URL_TEMPLATE = "https://podcasts.apple.com/us/podcast/id{}"


# pylint: disable=too-many-instance-attributes
@dataclass
class Podcast:
    """Podcast metadata."""

    # see https://github.com/schemaorg/schemaorg/issues/373
    id: int  # pylint: disable=invalid-name
    name: str
    author: str
    url: str
    feed: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    country: Optional[str] = None
    episode_count: Optional[int] = None


# pylint: disable=too-few-public-methods
class ItunesPodcast:
    """iTunes podcast description."""

    def __init__(self, source: dict):
        self._source = source

    def as_podcast(self) -> Podcast:
        """Converts iTunes description to Podcast object."""

        id_ = self._source["collectionId"]
        name = self._source["collectionName"]
        author = self._source["artistName"]
        url = URL_TEMPLATE.format(id_)
        podcast = Podcast(id=id_, name=name, author=author, url=url)
        podcast.feed = self._source.get("feedUrl")
        podcast.category = self._source.get("primaryGenreName")
        podcast.image = self._source.get("artworkUrl600")
        podcast.country = self._source.get("country")
        podcast.episode_count = self._source.get("trackCount")
        return podcast


class ItunesResults:
    """iTunes search results collection."""

    def __init__(self, source: dict):
        self.items = source.get("results", [])

    def as_podcasts(self) -> List[Podcast]:
        """Converts iTunes search results to Podcast list."""

        podcast_items = filter(ItunesResults._is_podcast, self.items)
        return [ItunesPodcast(item).as_podcast() for item in podcast_items]

    @staticmethod
    def _is_podcast(item):
        return item.get("wrapperType") == "track" and item.get("kind") == "podcast"


def search(query: str, country: str = "us", limit: int = 5) -> List[Podcast]:
    """
    Search podcast by query.

    Arguments:
    query   -- search string (name, author etc)
    country -- ISO alpha-2 country code
    limit   -- max number or search results
    """

    params = {"term": query, "country": country, "limit": limit, "media": "podcast"}
    response = http.get(url=SEARCH_URL, params=params)
    return ItunesResults(response).as_podcasts()


def get(ident: int) -> Optional[Podcast]:
    """Get podcast by iTunes ID."""

    params = {"id": ident}
    response = http.get(url=GET_URL, params=params)
    podcasts = ItunesResults(response).as_podcasts()
    return podcasts[0] if podcasts else None
