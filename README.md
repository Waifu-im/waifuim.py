# horiapi.py
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/horiapi.py?style=flat-square)](https://pypi.org/project/horiapi.py/)
[![PyPI](https://img.shields.io/pypi/v/horiapi.py?style=flat-square)](https://pypi.org/project/horiapi.py/)
[![License](https://img.shields.io/github/license/Buco/horiapi.py?style=flat-square)](https://github.com/Bucolo/horiapi.py/blob/main/LICENSE)

A Python wrapper for hori API.

## Table of Contents
- [Installation](#Installation)
- [Usage](#Usage)
- [License](#License)

## Installation
**Python 3.6 or higher is required.**

Install from PyPI
```shell
$ pip install horiapi.py
```

Install from source
```shell
$ pip install git+https://github.com/Bucolo/horiapi.py
```

## Usage
For now you can only use HoriAioClient wich is async. Maybe a sync client will be released in the future.

### Examples with HoriAioClient
```python
import asyncio

from horiapi import HoriAioClient


async def main():
    async with HoriAioClient() as haioct:

        # Get the json that the api return for the waifu tag
        waifujson= await haioct.sfw('waifu',raw=True)

        # Get one random image url for the waifu tag
        waifu_url = await haioct.sfw('waifu')

        # Get 30 images url for the waifu tag (12 is the tag id)
        waifulist= await haioct.nsfw(12,many=True)

        # Get one ero image excluding some files and the .gif extension
        ero = await haioct.nsfw('ero',exclude=['file1','file2.png','file3.jpeg'],gif=False)

        # Get your gallery (returns a dict)
        gallery=await haioct.fav(insert=['file1','file2.png','file3.jpeg'],delete=['file1','file2.png','file3.jpeg'],newtoken="The new token you want to use from now on instead of the one passed at the begining (or not).")

        #get the endpoints
        endpoints=await haioct.endpoints(full=True) #it is optional you can simply not set it to True and get the endpoints without details.

asyncio.run(main())
```
```python
import asyncio

from horiapi import HoriAioClient


async def main():
    haioct=HoriAioClient()
    # Get the json that the api return for the waifu tag
    waifujson= await haioct.sfw('waifu',raw=True)

    # Get one random image url for the waifu tag
    waifu_url = await haioct.sfw('waifu')

    # Get 30 images url for the waifu tag (12 is the tag id)
    waifulist= await haioct.nsfw('waifu',many=True)

    # Get one ero image excluding some files and the .gif extension
    ero = await haioct.nsfw('ero',exclude=['file1','file2.png','file3.jpeg'],gif=False)

    # Get your gallery (returns a dict)
    gallery=await haioct.fav(insert=['file1','file2.png','file3.jpeg'],delete=['file1','file2.png','file3.jpeg'],newtoken="The new token you want to use from now on instead of the one passed at the begining (or not).")

    # Get the endpoints
    endpoints=await haioct.endpoints(full=True) #it is optional you can simply not set it to True and get the endpoints without details.
    await haioct.close()

asyncio.run(main())
```

### Some interesting attributes
You can pass some useful kwargs to the class

```python
import aiohttp

from horiapi import HoriAioClient

haioct = HoriAioClient(session=aiohttp.ClientSession(),appname="MyDiscordBot",token="The Token that fav will use if newtoken isn't provided.",maintenance_error="The error message that you want to raise if the api is returning a 502.")

# ...
```

## License
MIT © [Buco](https://github.com/Bucolo/horiapi.py/blob/main/LICENSE)
