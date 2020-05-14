from unittest.mock import patch
from urllib.error import HTTPError, URLError
import pytest
from podsearch import http


def test_get():
    with patch("urllib.request.urlopen") as mock:
        mock.return_value.__enter__.return_value.read.return_value = """
{
    "resultCount": 1,
    "results": [
        {
            "collectionId": 979020229,
            "artistName": "Michael Kennedy (@mkennedy)",
            "collectionName": "Talk Python To Me",
            "collectionViewUrl": "https://podcasts.apple.com/us/podcast/id979020229?uo=4",
            "feedUrl": "https://talkpython.fm/episodes/rss",
            "primaryGenreName": "Technology",
            "artworkUrl600": "https://whatever/image/979020229.png"
        }
    ]
}
"""
        response = http.get(
            "https://itunes.apple.com/search", {"term": "talk python", "media": "podcast"}
        )
        req = mock.call_args[0][0]
        assert req.full_url == "https://itunes.apple.com/search?term=talk+python&media=podcast"
        assert "resultCount" in response
        assert "results" in response
        assert response["resultCount"] == 1


def test_network_error():
    with patch("urllib.request.urlopen") as mock:
        mock.side_effect = URLError(reason="certificate verify failed")
        with pytest.raises(Exception) as exc:
            http.get("https://itunes.apple.com/search", {"term": "python"})
        assert str(exc.value) == "Network error: certificate verify failed"


def test_http_error():
    with patch("urllib.request.urlopen") as mock:
        mock.return_value.__enter__.return_value.read.side_effect = HTTPError(
            "https://itunes.apple.com/search", 503, "Service Unavailable", {}, None
        )
        with pytest.raises(Exception) as exc:
            http.get("https://itunes.apple.com/search", {"term": "python"})
        assert str(exc.value) == "HTTP error 503: Service Unavailable"


def test_json_decode_error():
    with patch("urllib.request.urlopen") as mock:
        mock.return_value.__enter__.return_value.read.return_value = "hi there"
        with pytest.raises(Exception) as exc:
            http.get("https://itunes.apple.com/search", {"term": "python"})
        assert str(exc.value).startswith("Failed to parse response")
