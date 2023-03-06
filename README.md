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
Most of the methods returns an `Image` instance, the attributes are the same from the ones returned by the API.

### Examples with WaifuAioClient
```python
import asyncio

from waifuim import WaifuAioClient

async def main():

    wf = WaifuAioClient()
    
    # Get a completely random image
    image = await wf.search()
    
    # Get an image by tags
    image = await wf.search(
        included_tags=['waifu','maid'],
        excluded_tags=['ero'],
    )
    
    # Get sfw waifu images ordered by FAVORITES
    images = await wf.search(
        included_tags=['waifu'],
        is_nsfw='null',
        many=True,
        order_by='FAVORITES',
    )
    
    # Get a user favorites
    favorites = await wf.fav(
        token='if not provided, use the one in the client constructor',
    )
    
    # Edit your favorites
    await wf.fav_delete(3133)
    await wf.fav_insert(
        3133,
        user_id=11243585148445,
        token='user_id and token are optional',
    )
    fav_state = await wf.fav_toggle(4401)
    # will be equal to 'INSERTED' or 'DELETED'
 
    await wf.close()
    
    # You can also use a context manager but for multiple request it is not recommended
    
    async with WaifuAioClient() as wf:
        # Do your stuff

asyncio.run(main())
```

### The Image and Tag instance
In most of the case the methods will return an `Image` instance.
The attributes are the same as the json keys that the api returns.
```python

image = await wf.search()
>>> <waifuim.types.Image object at 0x76217ccf10>

image.url
>>> 'https://cdn.waifu.im/1982.jpg'

str(image)
>>> 'https://cdn.waifu.im/1982.jpg'

image.signature
>>> aa48cd9dc6b64367

image.tags[0]
>>> <waifuim.types.Tag object at 0x73214ccf10>

image.tags[0].name
>>> 'waifu'
```

### Some useful kwargs in the constructor
```python
from waifuim import WaifuAioClient

wf = WaifuAioClient(
    session=an_aiohttpClientSession_created_asynchronously,
    app_name="TheNameOfYourApplication",
    token="The default token to use in routes requiring authentication.",
)

# ...
```

## License
MIT © [Buco](https://github.com/Waifu-im/waifuim.py/blob/main/LICENSE)
