"""MIT License

Copyright (c) 2021 Buco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
import asyncio
from typing import (
    Optional,
    Union,
    Any,
    Dict,
    List
)

import aiohttp

from .exceptions import APIException,NoToken
from .utils import APIBaseURL,requires_token




class WaifuAioClient:
    def __init__(
        self,
        session: aiohttp.ClientSession = None,
        token: Optional[str] = None,
        appname: Optional[str] = None,

    ):
        """Asynchronous wrapper client for waifu.im API.
        This class is used to interact with the API (http requests).
        Attributes:
            session: An aiohttp session.
            token: your API token.(its optional since you only use it for the private gallery endpoint /fav/)
            appname: the name of your app in the user agent (please use it its easyer to identify you in the logs).
        """
        self.session=session
        self.token=token
        self.appname=appname

    async def __aenter__(self):
        return self

    async def __aexit__(self, exception_type, exception, exception_traceback):
        await self.close()

    async def close(self) -> None:
        """Closes the aiohttp session (call it when you're sure you wont do any request anymore)."""
        if self.session is not None:
            await self.session.close()

    async def _get_session(self):
        if not self.session:
            self.session=aiohttp.ClientSession()
        return self.session

    async def _make_request(self, url: str, method: str, *args, **kwargs):
        response = await getattr(await self._get_session(), method)(url, *args, **kwargs)
        infos= await response.json()
        if response.status==200:
            return infos
        else:
            raise APIException(response.status,response.reason,infos['error'])

    def _create_params(self,**kwargs):
        rt={k:','.join(i) if isinstance(i,list) else str(i) for k,i in kwargs.items() if i}
        if rt:
            return rt

    async def _fetchtag(self, type_, tag, raw, exclude, gif, many):
        """process the request for a specific tag and check if everything is correct."""
        params=self._create_params(exclude=exclude,gif=gif,many=many)
        headers=self._create_params(**{'User-Agent':f'aiohttp/{aiohttp.__version__}; {self.appname}' if self.appname else None})
        infos= await self._make_request(f"{APIBaseURL}{type_}/{tag}/",'get',params=params,headers=headers)
        if raw:
            return infos
        return [im.get('url') for im in infos.get('tags')[0].get('images')] if many else infos.get('tags')[0].get('images')[0].get('url')


    async def sfw(self, tag: Union[int,str], raw: bool=False, exclude: List[str]=None, gif: bool=None, many: bool=None):
        """Gets a single or multiple unique SFW images of the specific category.
        Args:
            tag: The tag to request.
            
        Kwargs:
            raw: if whether or not you want the wrapper to return the entire json or just the picture url.
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            exclude: A list of URL's that you do not want to get.
            raw: If False is provided prevent the API to return .gif files, else if True is provided force it to do so if nothing is provided then it is completly random.
        Returns:
            A single or a list of image URL's.
        Raises:
            APIException: If the API response contains an error.
        """
        data = await self._fetchtag('sfw',tag,raw,exclude,gif,many)
        return data

    async def nsfw(self, tag: Union[int,str], raw: bool=False, exclude: List[str]=None, gif: bool=None, many: bool=None):
        """Gets a single or multiple unique NSFW (Not Safe for Work) images of the specific category.
        Args:
            tag: The tag to request.
            
        Kwargs:
            raw: if whether or not you want the wrapper to return the entire json or just the picture url.
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            exclude: A list of URL's that you do not want to get.
            raw: If False is provided prevent the API to return .gif files, else if True is provided force it to do so if nothing is provided then it is completly random.
        Returns:
            A single or a list of image URL's.
        Raises:
            APIException: If the API response contains an error.
        """
        return await self._fetchtag('nsfw',tag,raw,exclude,gif,many)

    @requires_token
    async def fav(self, user_id: str=None,toggle : List[str]=None,insert: List[str]=None, delete: List[str]=None, token: str=None):
        """Get your favorite gallery.""

        Kwargs:
            user_id: The user's id you want to access the gallery (only for trusted apps).
            toggle: A list of file names that you want to add if they do not already exist in, else remove, to your gallery in the same time.
            insert: A list of file names that you want to add to your gallery in the same time.
            delete: A list of file names that you want to remove from your gallery in the same time.
            token: The token that will be use for this request only, this doesnt change the token you passed in the class.
        Returns:
            A dictionnary containing the json the API returned.
        Raises:
            APIException: If the API response contains an error.
        """
        params=self._create_params(id=user_id,toggle=toggle,insert=insert,delete=delete)
        headers=self._create_params(**{'User-Agent':f'aiohttp/{aiohttp.__version__}; {self.appname}' if self.appname else None,'Authorization':f'Bearer {token if token else self.token}'})
        return await self._make_request(f"{APIBaseURL}fav/",'get',params=params,headers=headers)

    async def info(self,images :List[str]=None):
        """Fetch the images data (as if you where requesting a gallery containing only those images
        Kwargs:
            images : A list of images filenames to provide.
        Raises:
            APIException: If the API response contains an error.
        """
        params=self._create_params(images=images)
        headers=self._create_params(**{'User-Agent':f'aiohttp/{aiohttp.__version__}; {self.appname}' if self.appname else None})
        return await self._make_request(f"{APIBaseURL}info/",'get',params=params,headers=headers)


    async def endpoints(self, full=False):
        """Gets the API endpoints.

        Kwargs:
            full: if whether or not you want the wrapper to return the endpoints with all the tag informations or just the availiables tag.

        Returns:
            A dictionnary containing the API endpoints.
        Raises:
            APIException: If the API response contains an error.
        """
        params=self._create_params(full=full)
        headers=self._create_params(**{'User-Agent':f'aiohttp/{aiohttp.__version__}; {self.appname}' if self.appname else None})
        return await self._make_request(APIBaseURL+'endpoints/','get',headers=headers,params=params)



