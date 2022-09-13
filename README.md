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
Most of the methods returns an Image instance, the attributes are the same from the ones returned by the API.

### Examples with WaifuAioClient
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
    
    # Get a user favourites
    favs = await wf.fav(token='The user token if no token is provided it use the one in the client constructor')
    
    # Edit your favourites
    await wf.fav_delete('aa48cd9dc6b64367.jpg')
    await wf.fav_insert('aa48cd9dc6b64367',user_id=11243585148445,token='user_id and token are optional')
    fav_state = await wf.toggle('aa48cd9dc6b64367.jpg')
    # fav_state wil be equal to 'INSERTED' or 'DELETED'
    
    # Get information about one or multiple pictures (can also provide the image ID instead of file name)
    information = await wf.info(['aa48cd9dc6b64367.jpg',1982])
 
    await wf.close()
    
    # You can also use a context manager but for multiple request it is not recommended
    
    async with WaifuAioClient() as wf:
        # Do your stuff

asyncio.run(main())
```

### The Image and Tag instance
In most of the case the methods will return an Image instance.
The attributes are the same as the json keys that the api returns.
```python

image = await wf.random()
>>> <waifuim.types.Image object at 0x76217ccf10>

image.url
>>> 'https://cdn.waifu.im/aa48cd9dc6b64367jpg'

str(image)
>>> 'https://cdn.waifu.im/aa48cd9dc6b64367jpg'

image.image_id
>>> 1982

image.tags[0]
>>> <waifuim.types.Tag object at 0x73214ccf10>
```

### Some useful kwargs in the constructor
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
