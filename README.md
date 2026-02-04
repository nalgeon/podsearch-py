# Podcast searcher

> Search any podcast in iTunes library

`podsearch` finds podcasts via [iTunes Search API](https://developer.apple.com/library/archive/documentation/AudioVideo/Conceptual/iTuneSearchAPI/index.html).

Search parameters:

-   _query_ - search string (name, author etc)
-   _country_ - ISO alpha-2 country code (us, de, fr etc), default: us
-   _limit_ - maximum number or search results, default: 5

Returned attributes for each podcast:

-   _id_ - iTunes ID (e.g., `979020229`)
-   _name_ - podcast name (`Talk Python To Me`)
-   _author_ - author name (`Michael Kennedy (@mkennedy)`)
-   _url_ - Apple Podcasts URL (`https://podcasts.apple.com/us/podcast/id979020229`)
-   _feed_ - podcast RSS URL (`https://talkpython.fm/episodes/rss`)
-   _category_ - main category (`Technology`)
-   _image_ - 600x600px image URL (`https://is4-ssl.mzstatic.com/image/.../600x600bb.jpg`)
-   _country_ - ISO alpha-3 country code (`USA`)
-   _episode_count_ - episode count this year (`26`)

## Installation

```sh
pip install podsearch
```

## Usage

Search podcasts by query:

```python
>>> import podsearch
>>> podcasts = podsearch.search("python", country="us", limit=10)
>>> podcasts[0].name
'Talk Python To Me'
>>> podcasts[0].author
'Michael Kennedy (@mkennedy)'
>>> podcasts[0].url
'https://podcasts.apple.com/us/podcast/id979020229'
```

Retrieve podcast by iTunes ID:

```python
>>> import podsearch
>>> podcast = podsearch.get(979020229)
>>> podcast.name
'Talk Python To Me'
```

## Development setup

```sh
$ python3 -m venv env
$ . env/bin/activate
$ make deps
$ tox
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
