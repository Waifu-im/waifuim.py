# waifuim.py
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/waifuim.py?style=flat-square)](https://pypi.org/project/waifuim.py/)
[![PyPI](https://img.shields.io/pypi/v/waifuim.py?style=flat-square)](https://pypi.org/project/waifuim.py/)
[![License](https://img.shields.io/github/license/Bucolo/waifuim.py?style=flat-square)](https://github.com/Bucolo/waifuim.py/blob/main/LICENSE)

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
$ pip install git+https://github.com/Bucolo/waifuim.py
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
        waifujson= await wf.sfw('waifu',raw=True)

        # Get one random image url for the waifu tag
        waifu_url = await wf.sfw('waifu')

        # Get 30 images url for the waifu tag (12 is the tag id)
        waifulist= await wf.nsfw(12,many=True)

        # Get one ero image excluding some files and the .gif extension
        ero = await wf.nsfw('ero',exclude=['file1','file2.png','file3.jpeg'],gif=False)

        # Get your gallery (returns a dict)
        gallery=await wf.fav(insert=['file1','file2.png','file3.jpeg'],delete=['file1','file2.png','file3.jpeg'],token="The token that will be used only for this request.")

        #get the endpoints
        endpoints=await wf.endpoints(full=True) #it is optional you can simply not set it to True and get the endpoints without details.

asyncio.run(main())
```
```python
import asyncio

from waifuim import WaifuAioClient


async def main():
    wf=WaifuAioClient()
    # Get the json that the api return for the waifu tag
    waifujson= await wf.sfw('waifu',raw=True)

    # Get one random image url for the waifu tag
    waifu_url = await wf.sfw('waifu')

    # Get 30 images url for the waifu tag (12 is the tag id)
    waifulist= await wf.nsfw('waifu',many=True)

    # Get one ero image excluding some files and the .gif extension
    ero = await wf.nsfw('ero',exclude=['file1','file2.png','file3.jpeg'],gif=False)

    # Get your gallery (returns a dict)
    gallery=await wf.fav(insert=['file1','file2.png','file3.jpeg'],delete=['file1','file2.png','file3.jpeg'],token="The token that will be used only for this request.")

    # Get the endpoints
    endpoints=await wf.endpoints(full=True) #it is optional you can simply not set it to True and get the endpoints without details.
    await wf.close()

asyncio.run(main())
```

### Some interesting attributes
You can pass some useful kwargs to the class

```python
import aiohttp

from waifuim import WaifuAioClient

wf = WaifuAioClient(session=aiohttp.ClientSession(),appname="MyDiscordBot",token="The Token that fav will use if token isn't provided.",maintenance_error="The error message that you want to raise if the api is returning a 502.")

# ...
```

## License
MIT © [Buco](https://github.com/Bucolo/waifuim.py/blob/main/LICENSE)
