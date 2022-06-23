# waifuim.py
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/waifuim.py?style=flat-square)](https://pypi.org/project/waifuim.py/)
[![PyPI](https://img.shields.io/pypi/v/waifuim.py?style=flat-square)](https://pypi.org/project/waifuim.py/)
[![License](https://img.shields.io/github/license/Waifu-im/waifuim.py?style=flat-square)](https://github.com/Waifu-im/waifuim.py/blob/main/LICENSE)

A Python wrapper for waifu.im API.

## Table of Contents
- [Installation](#Installation)
- [Usage](#Usage)
- [License](#License)

## Installation
**Python 3.6 or higher is required.**

Install from PyPI
```shell
$ pip install waifuim.py
```

Install from source
```shell
$ pip install git+https://github.com/Waifu-im/waifuim.py
```

## Usage
For now, you can only use WaifuAioClient which is async. Maybe a sync client will be released in the future.

### Examples with WaifuAioClient
```python
import asyncio

from waifuim import WaifuAioClient


async def main():
    # Depending on your usage of the Wrapper It's recommended to store the Client and not to open a session each time.
    async with WaifuAioClient() as wf:
        # Get a completely random image
        image = await wf.random()
        # Get an image by tags
        image = await wf.random(selected_tags=['waifu','maid'],excluded_tags=['ero'],excluded_files=['file1.notneeded'])
        # Get sfw waifu images ordered by FAVOURITES
        images = await wf.random(selected_tags=['waifu'],is_nsfw=False,many=True,order_by='FAVOURITES')
        # Get a user favourites images
        favs = await wf.fav(token='The user token if no token is provided it use the one in the client constructor')
        


asyncio.run(main())
```

```python
import asyncio

from waifuim import WaifuAioClient


async def main():
    wf = WaifuAioClient()
    # Get a completely random image
    image = await wf.random()
    # Get an image by tags
    image = await wf.random(selected_tags=['waifu','maid'],excluded_tags=['ero'])
    # Get sfw waifu images ordered by FAVOURITES
    images = await wf.random(selected_tags=['waifu'],is_nsfw='null',many=True,order_by='FAVOURITES')
    # Get a user favourites images
    favs = await wf.fav(token='The user token if no token is provided it use the one in the client constructor')
    await wf.close()


asyncio.run(main())
```

### Some interesting attributes
You can pass some useful kwargs to the class

```python
from waifuim import WaifuAioClient

wf = WaifuAioClient(
    session=an_aiohttpClientSession_created_asynchronously,
    appname="TheNameOfYourApplication",
    token="The default token to use in routes requiring authentication.",
)

# ...
```

## License
MIT © [Buco](https://github.com/Waifu-im/waifuim.py/blob/main/LICENSE)
