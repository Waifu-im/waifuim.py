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
For now you can only use WaifuAioClient wich is async. Maybe a sync client will be released in the future.

### Examples with WaifuAioClient
```python
import asyncio

from waifuim import WaifuAioClient


async def main():
    async with WaifuAioClient() as wf:

        # Get the json that the api return for the waifu tag
        waifujson= await wf.sfw('waifu',raw = True)

        # Get one random image url for the waifu tag
        waifu_url = await wf.sfw('waifu')

        # Get 30 images url for the waifu tag (12 is the tag id)
        waifulist= await wf.nsfw(12, many = True)

        # Get one ero image excluding some files and the .gif extension
        ero = await wf.nsfw('ero',exclude = ['file1', 'file2.png'], gif = False)

        # Get your gallery (returns a dict)
        gallery=await wf.fav(toggle = ['file20'], insert = ['file1'], token = "A token")

        #get the endpoints
        endpoints=await wf.endpoints(full = True) #it is optional

        # Get some informations about one or multiple images
        info=await wf.info(images = ["file1.png" ,"file2"])

        # Get the 30 most liked waifu images
        top=await wf.sfw("waifu", many = True, top = True)

        # Get completly random images, you can use same kwargs as sfw and nsfw
        random=await wf.random()

asyncio.run(main())
```
```python
import asyncio

from waifuim import WaifuAioClient


async def main():
    wf=WaifuAioClient()
    # Get the json that the api return for the waifu tag
    waifujson= await wf.sfw('waifu', raw = True)

    # Get one random image url for the waifu tag
    waifu_url = await wf.sfw('waifu')

    # Get 30 images url for the waifu tag (12 is the tag id)
    waifulist= await wf.nsfw('waifu', many = True)

    # Get one ero image excluding some files and the .gif extension
    ero = await wf.nsfw('ero', exclude = ['file1', 'file2.png', 'file3.jpeg'], gif = False)

    # Get your gallery (returns a dict)
    gallery=await wf.fav(toggle = ['file20'], delete = ['file1'])

    # Get the endpoints
    endpoints=await wf.endpoints(full=True) #it is optional

    # Get some informations about one or multiple images
    info=await wf.info(images = ["file1.png", "file2"])

    # Get the 30 most liked waifu images
    top=await wf.sfw("waifu", many = True, top = True)

    # Get completly random images, you can use same kwargs as sfw and nsfw
    random=await wf.random()

    await wf.close()

asyncio.run(main())
```

### Some interesting attributes
You can pass some useful kwargs to the class

```python
from waifuim import WaifuAioClient

wf = WaifuAioClient(session = an_aiohttpClientSession_created_asynchronously,
    appname = "TheNameOfYourApplication",
    token = "The default token to use in routes requiring authentifiction.")

# ...
```

## License
MIT © [Buco](https://github.com/Waifu-im/waifuim.py/blob/main/LICENSE)
