"""
Podcast searching via iTunes.
See https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html  # noqa: E501  pylint: disable=line-too-long
for iTunes API Description.
"""

from dataclasses import dataclass
from typing import List, Optional
from podsearch import http

SEARCH_URL = "https://itunes.apple.com/search"
URL_TEMPLATE = "https://podcasts.apple.com/us/podcast/id{}"


# pylint: disable=too-many-instance-attributes
@dataclass
class Podcast:
    """Podcast metadata."""

    # see https://github.com/schemaorg/schemaorg/issues/373
    id: str  # pylint: disable=invalid-name
    name: str
    author: str
    url: str
    feed: Optional[str] = None
    category: Optional[str] = None
    image: Optional[str] = None
    country: Optional[str] = None
    episode_count: Optional[int] = None


def search(query: str, country: str = None, limit: int = 5) -> List[Podcast]:
    """
    Search podcast by query.

    Arguments:
    query   -- search string (name, author etc)
    country -- ISO alpha-2 country code
    limit   -- max number or search results
    """

    params = {"term": query, "limit": limit, "media": "podcast"}
    if country:
        params["country"] = country
    response = http.get(url=SEARCH_URL, params=params)
    return _parse(response)


def _parse(response: dict) -> List[Podcast]:
    result_count = response.get("resultCount")
    if not result_count:
        return []
    return [_parse_item(item) for item in response.get("results", [])]


def _parse_item(item: dict) -> Podcast:
    try:
        id_ = str(item["collectionId"])
        name = item["collectionName"]
        author = item["artistName"]
        url = URL_TEMPLATE.format(id_)
        podcast = Podcast(id=id_, name=name, author=author, url=url)
        podcast.feed = item.get("feedUrl")
        podcast.category = item.get("primaryGenreName")
        podcast.image = item.get("artworkUrl600")
        podcast.country = item.get("country")
        podcast.episode_count = item.get("trackCount")
        return podcast
    except LookupError as exc:
        raise Exception(f"Failed to parse podcast item: {exc}\n{item}")
