from unittest.mock import patch
import pytest
import podsearch


def test_search():
    with patch("podsearch.http.get") as mock:
        mock.return_value = {
            "resultCount": 2,
            "results": [
                {
                    "wrapperType": "track",
                    "kind": "podcast",
                    "collectionId": 979020229,
                    "artistName": "Michael Kennedy (@mkennedy)",
                    "collectionName": "Talk Python To Me",
                    "collectionViewUrl": "https://podcasts.apple.com/us/podcast/id979020229?uo=4",
                    "feedUrl": "https://talkpython.fm/episodes/rss",
                    "primaryGenreName": "Technology",
                    "artworkUrl600": "https://whatever/image/979020229.png",
                    "trackCount": 26,
                    "country": "USA",
                },
                {
                    "wrapperType": "track",
                    "kind": "podcast",
                    "collectionId": 981834425,
                    "artistName": "Tobias Macey",
                    "collectionName": "The Python Podcast.__init__",
                    "collectionViewUrl": "https://podcasts.apple.com/us/podcast/id981834425?uo=4",
                    "feedUrl": "https://www.podcastinit.com/feed/mp3/",
                    "primaryGenreName": "Technology",
                    "artworkUrl600": "https://whatever/image/981834425.png",
                    "trackCount": 16,
                    "country": "USA",
                },
            ],
        }

        podcasts = podsearch.search("Python")
        assert len(podcasts) == 2
        talkpython = podcasts[0]
        assert talkpython.id == 979020229
        assert talkpython.name == "Talk Python To Me"
        assert talkpython.author == "Michael Kennedy (@mkennedy)"
        assert talkpython.url == "https://podcasts.apple.com/us/podcast/id979020229"
        assert talkpython.feed == "https://talkpython.fm/episodes/rss"
        assert talkpython.category == "Technology"
        assert talkpython.image == "https://whatever/image/979020229.png"
        assert talkpython.country == "USA"
        assert talkpython.episode_count == 26


def test_search_defaults():
    with patch("podsearch.http.get") as mock:
        podsearch.search("Python")
        mock.assert_called_with(
            url=podsearch.searcher.SEARCH_URL,
            params={"term": "Python", "country": "us", "limit": 5, "media": "podcast"},
        )


def test_search_params():
    with patch("podsearch.http.get") as mock:
        podsearch.search("Python", country="us", limit=10)
        mock.assert_called_with(
            url=podsearch.searcher.SEARCH_URL,
            params={"term": "Python", "country": "us", "limit": 10, "media": "podcast"},
        )


def test_nothing_found():
    with patch("podsearch.http.get") as mock:
        mock.return_value = {"resultCount": 0, "results": []}
        podcasts = podsearch.search("Python")
        assert len(podcasts) == 0


def test_failed():
    with patch("podsearch.http.get") as mock:
        mock.side_effect = Exception()
        with pytest.raises(Exception):
            podsearch.search("Python")


def test_parsing_failed():
    with patch("podsearch.http.get") as mock:
        mock.return_value = {
            "resultCount": 1,
            "results": [{"wrapperType": "track", "kind": "podcast", "collectionId": 979020229}],
        }
        with pytest.raises(Exception):
            podsearch.search("Python")
