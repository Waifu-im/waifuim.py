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

import contextlib
from types import TracebackType
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Type,
    Union,
)

import aiohttp

from .exceptions import APIException
from .utils import APIBaseURL, requires_token
from .moduleinfo import __version__
from .exceptions import NoToken


class WaifuAioClient(contextlib.AbstractAsyncContextManager):
    def __init__(
            self,
            session: aiohttp.ClientSession = None,
            token: Optional[str] = None,
            appname: str = f'aiohttp/{aiohttp.__version__}; waifuim.py/{__version__}',
    ) -> None:
        """Asynchronous wrapper client for waifu.im API.
        This class is used to interact with the API (http requests).
        Attributes:
            session: An aiohttp session.
            token: your API token.(its optional since you only use it for the private gallery endpoint /fav/)
            appname: the name of your app in the user agent (please use it its easier to identify you in the logs).
        """
        self.session = session
        self.token = token
        self.appname = appname

    async def __aexit__(
            self,
            exception_type: Type[Exception],
            exception: Exception,
            exception_traceback: TracebackType,
    ) -> None:
        await self.close()

    @staticmethod
    def _create_headers(**kwargs) -> Optional[Dict[str, str]]:
        rt = {k: str(i) for k, i in kwargs.items() if i or isinstance(i, bool)}
        if rt:
            return rt

    @staticmethod
    def _create_params(**kwargs) -> Optional[Dict[str, str]]:
        string = ''
        first = True
        for k, i in kwargs.items():
            if i or isinstance(i, bool):
                string += '?' if first else '&'
                first = False
                string += k + '=' + i
        return string

    async def close(self) -> None:
        """Closes the aiohttp session (call it when you're sure you won't do any request anymore)."""
        if self.session is not None:
            await self.session.close()

    async def _get_session(self) -> aiohttp.ClientSession:
        if not self.session:
            self.session = aiohttp.ClientSession()
        return self.session

    async def _make_request(
            self,
            url: str,
            method: str,
            *args,
            **kwargs,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        session = await self._get_session()
        async with session.request(method.upper(), url, *args, **kwargs) as response:
            if response.status == 204:
                return
            infos = await response.json()
            if response.status in {200, 201}:
                return infos
            else:
                raise APIException(response.status, infos['message'])

    async def random(
            self,
            selected_tags: List[str] = None,
            excluded_tags: List[str] = None,
            excluded_files: List[str] = None,
            is_nsfw: bool = None,
            many: bool = None,
            order_by: str = None,
            gif: bool = None,
            full: str = None,
            token: str = None,
            raw: bool = False,
    ) -> Dict:
        """Gets a single or multiple images from the API.
        Kwargs:
            selected_tags : The tag(s) that you want to select
            excluded_tags: The tag(s) that you want to exclude
            excluded_files: A list of files that you do not want to get.
            is_nsfw: If False is provided prevent the API to return nsfw files, else if True is provided force it to do
            so, if nothing (or None) is provided then no filter is applied.
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            order_by: Order the images according to the value given (see the docs for the accepted values)
            gif: If False is provided prevent the API to return .gif files, else if True is provided force it to do so
            if nothing (or None) is provided then no filter is applied.
            full: Do not limit the result length (only for admins)
            raw: whether you want the wrapper to return the entire json or just the picture url.
        Returns:
            A single or a list of image URLs.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(selected_tags=selected_tags,
                                     excluded_tags=excluded_tags,
                                     excluded_files=excluded_files,
                                     is_nsfw=is_nsfw,
                                     many=many,
                                     order_by=order_by,
                                     gif=gif,
                                     full=full
                                     )
        headers = self._create_headers(**{'User-Agent': self.appname})
        if full:
            if not token and not self.token:
                raise NoToken(message="the 'full' query string is only accessible to admins and needs a token")
            headers += {'Authorization': f'Bearer {token if token else self.token}'}
        infos = await self._make_request(f"{APIBaseURL}random/+{params}", 'get', headers=headers)
        if raw:
            return infos
        return [im['url'] for im in infos['images']] if many else infos['images'][0]['url']

    @requires_token
    async def fav(
            self,
            user_id: str = None,
            toggle: List[str] = None,
            insert: List[str] = None,
            delete: List[str] = None,
            token: str = None,
    ) -> Dict:
        """Get your favorite gallery.""

        Kwargs:
            user_id: The user's id you want to access the gallery (only for trusted apps).
            toggle: A list of file names that you want to add if they do not already exist in, else remove, to your
            gallery in the same time.
            insert: A list of file names that you want to add to your gallery in the same time.
            delete: A list of file names that you want to remove from your gallery in the same time.
            token: The token that will be use for this request only, this doesn't change the token passed in __init__.
        Returns:
            A dictionary containing the json the API returned.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(user_id=user_id, toggle=toggle, insert=insert, delete=delete)
        headers = self._create_headers(
            **{'User-Agent': self.appname, 'Authorization': f'Bearer {token if token else self.token}'})
        return await self._make_request(f"{APIBaseURL}fav/{params}", 'get', headers=headers)

    async def info(self, images: List[str]) -> Dict:
        """Fetch the images' data (as if you were requesting a gallery containing only those images)
        args:
            images : A list of images filenames to provide.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(images=images)
        headers = self._create_headers(**{'User-Agent': self.appname})
        return await self._make_request(f"{APIBaseURL}info/{params}", 'get', headers=headers)

    @requires_token
    async def report(
            self,
            image: str,
            description: str = None,
            user_id: str = None,
    ) -> Dict:
        """Report an image and returns the report information
        Args:
            image: The image to report.
        Kwargs:
            description: The optional reason why to report the image.
            user_id: The report author.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(image=image, description=description, user_id=user_id)
        headers = self._create_headers(**{'User-Agent': self.appname, 'Authorization': f'Bearer {self.token}'})
        return await self._make_request(f"{APIBaseURL}report/{params}", 'get', headers=headers)

    async def endpoints(self, full=False) -> Dict:
        """Gets the API endpoints.

        Kwargs:
            full: if whether you want the wrapper to return the endpoints with all the tag information or just the
            available tags.

        Returns:
            A dictionary containing the API endpoints.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(full=full)
        headers = self._create_headers(**{'User-Agent': self.appname})
        return await self._make_request(APIBaseURL + f'endpoints/{params}', 'get', headers=headers)
