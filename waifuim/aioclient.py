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
from .moduleinfo import __version__


class WaifuAioClient:
    def __init__(
        self,
        session: aiohttp.ClientSession = None,
        token: Optional[str] = None,
        appname = f'aiohttp/{aiohttp.__version__}; waifuim.py/{__version__}'

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

    async def __aexit__(
        self,
        exception_type,
        exception,
        exception_traceback
    ) -> None:
        await self.close()


    def _create_params(self,**kwargs):
        rt={k:','.join(i) if isinstance(i, list) else str(i) for k,i in kwargs.items() if i}
        if rt:
            return rt

    async def close(self) -> None:
        """Closes the aiohttp session (call it when you're sure you wont do any request anymore)."""
        if self.session is not None:
            await self.session.close()

    async def _get_session(self):
        if not self.session:
            self.session=aiohttp.ClientSession()
        return self.session

    async def _make_request(
        self,
        url: str,
        method: str,
        *args,
        **kwargs
    ):
        response = await getattr(await self._get_session(), method)(url, *args, **kwargs)
        infos= await response.json()
        if response.status==200:
            return infos
        else:
            raise APIException(response.status, infos['message'])

    async def _fetchtag(
        self,
        type_,
        tag,
        raw,
        exclude,
        gif,
        many,
        top
    ):
        """process the request for a specific tag and check if everything is correct."""
        params=self._create_params(exclude = exclude, gif = gif, many = many, top = top)
        headers=self._create_params(**{'User-Agent': self.appname})
        type_and_tag="random" if type_ is None or tag is None else type_+"/"+tag
        infos= await self._make_request(f"{APIBaseURL}{type_and_tag}/", 'get', params = params, headers = headers)
        if raw:
            return infos
        return [im['url'] for im in infos['images']] if many else infos['images'][0]['url']



    async def random(
        self,
        raw: bool = False,
        exclude: List[str] = None,
        gif: bool = None,
        many: bool = None,
        top: bool = None
    ) -> Dict:
        """Gets a single or multiple images from the API.            
        Kwargs:
            raw: if whether or not you want the wrapper to return the entire json or just the picture url.
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            top: Order by most liked image(s).
            exclude: A list of URL's that you do not want to get.
            gif: If False is provided prevent the API to return .gif files, else if True is provided force it to do so if nothing is provided then it is completly random.
        Returns:
            A single or a list of image URL's.
        Raises:
            APIException: If the API response contains an error.
        """
        return await self._fetchtag(None,None, raw, exclude, gif, many, top)

    async def sfw(
        self,
        tag: Union[int, str],
        raw: bool = False,
        exclude: List[str] = None,
        gif: bool = None,
        many: bool = None,
        top: bool = None
    ) -> Dict:
        """Gets a single or multiple unique SFW images of the specific category.
        Args:
            tag: The tag to request.
            
        Kwargs:
            raw: if whether or not you want the wrapper to return the entire json or just the picture url.
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            top: Order by most liked image(s).
            exclude: A list of URL's that you do not want to get.
            gif: If False is provided prevent the API to return .gif files, else if True is provided force it to do so if nothing is provided then it is completly random.
        Returns:
            A single or a list of image URL's.
        Raises:
            APIException: If the API response contains an error.
        """
        return await self._fetchtag('sfw', tag, raw, exclude, gif, many, top)

    async def nsfw(
        self,
        tag : Union[int, str], raw: bool = False,
        exclude : List[str] = None,
        gif : bool = None,
        many : bool = None,
        top : bool = None
    ) -> Dict:
        """Gets a single or multiple unique NSFW (Not Safe for Work) images of the specific category.
        Args:
            tag: The tag to request.
            
        Kwargs:
            raw: if whether or not you want the wrapper to return the entire json or just the picture url.
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            top: Order by most liked image(s).
            exclude: A list of URL's that you do not want to get.
            raw: If False is provided prevent the API to return .gif files, else if True is provided force it to do so if nothing is provided then it is completly random.
        Returns:
            A single or a list of image URL's.
        Raises:
            APIException: If the API response contains an error.
        """
        return await self._fetchtag('nsfw', tag, raw, exclude, gif, many, top)

    @requires_token
    async def fav(
        self,
        user_id : str = None,
        toggle : List[str] = None,
        insert : List[str] = None,
        delete : List[str] = None,
        token : str = None
    ) -> Dict:
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
        params=self._create_params(user_id = user_id, toggle = toggle, insert = insert, delete = delete)
        headers=self._create_params(**{'User-Agent' : self.appname, 'Authorization' : f'Bearer {token if token else self.token}'})
        return await self._make_request(f"{APIBaseURL}fav/", 'get', params = params, headers = headers)

    async def info(self, images : List[str] = None) -> Dict:
        """Fetch the images data (as if you where requesting a gallery containing only those images
        Kwargs:
            images : A list of images filenames to provide.
        Raises:
            APIException: If the API response contains an error.
        """
        params=self._create_params(images = images)
        headers=self._create_params(**{'User-Agent':self.appname})
        return await self._make_request(f"{APIBaseURL}info/", 'get', params = params, headers = headers)

    async def endpoints(self, full = False) -> Dict:
        """Gets the API endpoints.

        Kwargs:
            full: if whether or not you want the wrapper to return the endpoints with all the tag informations or just the availiables tag.

        Returns:
            A dictionnary containing the API endpoints.
        Raises:
            APIException: If the API response contains an error.
        """
        params=self._create_params(full = full)
        headers=self._create_params(**{'User-Agent' : self.appname})
        return await self._make_request(APIBaseURL + 'endpoints/', 'get', headers = headers, params = params)



