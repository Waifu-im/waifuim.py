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
from .types import Image, Tag
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
            exception_traceback,
    ) -> None:
        await self.close()

    @staticmethod
    def _create_headers(**kwargs) -> Optional[Dict]:
        rt = {k: str(i) for k, i in kwargs.items() if i or isinstance(i, bool)}
        if rt:
            return rt

    @staticmethod
    def _create_params(**kwargs) -> Optional[Dict]:
        rt = {}
        for k, i in kwargs.items():
            if isinstance(i, (list, tuple, set)):
                rt.update({k: list(i)})
            elif isinstance(i, Image):
                rt.update({k: i.file})
            elif i or isinstance(i, bool):
                rt.update({k: str(i)})
        if rt:
            return rt

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
    ) -> Dict:
        session = await self._get_session()
        async with session.request(method.upper(), url, *args, **kwargs) as response:
            if response.status == 204:
                return
            infos = await response.json()
            if response.status in {200, 201}:
                return infos
            elif response.status == 422:
                raise APIException(
                    response.status,
                    f'Error at {infos["detail"][0]["loc"][1]}: {infos["detail"][0]["msg"]}'
                )
            else:
                raise APIException(response.status, infos['detail'])

    async def random(
            self,
            selected_tags: List[str] = None,
            excluded_tags: List[str] = None,
            excluded_files: List[str] = None,
            is_nsfw: Union[bool, str] = None,
            many: bool = None,
            order_by: str = None,
            orientation: str = None,
            gif: bool = None,
            full: str = None,
            token: str = None,
            raw: bool = False,
    ) -> Union[List[Image], Image, Dict]:
        """Gets a single or multiple images from the API.
        Kwargs:
            selected_tags : The tag(s) that you want to select
            excluded_tags: The tag(s) that you want to exclude
            excluded_files: A list of files that you do not want to get.
            is_nsfw: If False is provided prevent the API to return nsfw files, else if True is provided force it to do
            so, if 'null' is provided it's random (Default fixed by the API, see the documentation).
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            order_by: Order the images according to the value given (see the docs for the accepted values)
            orientation: Choose the images orientation according to the value given (see the docs for the accepted values)
            gif: If False is provided prevent the API to return .gif files, else if True is provided force it to do so
            if nothing (or None) is provided then no filter is applied.
            full: Do not limit the result length (only for admins)
            raw : If True return the raw result.
        Returns:
            A single or a list of Image (find it in types.py).
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(selected_tags=selected_tags,
                                     excluded_tags=excluded_tags,
                                     excluded_files=excluded_files,
                                     is_nsfw=is_nsfw,
                                     many=many,
                                     order_by=order_by,
                                     orientation=orientation,
                                     gif=gif,
                                     full=full
                                     )
        headers = self._create_headers(**{'User-Agent': self.appname})
        if full:
            if not token and not self.token:
                raise NoToken(detail="the 'full' query string is only accessible to admins and needs a token")
            headers.update({'Authorization': f'Bearer {token if token else self.token}'})
        infos = await self._make_request(f"{APIBaseURL}random/", 'get', params=params, headers=headers)
        if raw:
            return infos
        images = [Image(im) for im in infos['images']]
        if len(images) > 1:
            return images
        return images[0]

    @requires_token
    async def fav(
            self,
            user_id: str = None,
            selected_tags: List[str] = None,
            excluded_tags: List[str] = None,
            excluded_files: List[str] = None,
            is_nsfw: Union[bool, str] = None,
            many: bool = None,
            order_by: str = None,
            orientation: str = None,
            gif: bool = None,
            token: str = None,
            raw: bool = False,
    ) -> Union[List[Image], Dict]:
        """Get your favourite gallery.""

        Kwargs:
            user_id: The user's id you want to access the gallery (only for trusted apps).
            selected_tags : The tag(s) that you want to select
            excluded_tags: The tag(s) that you want to exclude
            excluded_files: A list of files that you do not want to get.
            is_nsfw: If False is provided prevent the API to return nsfw files, else if True is provided force it to do
            so, if 'null' is provided it's random (Default fixed by the API, see the documentation).
            many: Get multiples images instead of a single one (see the api docs for the exact number).
            order_by: Order the images according to the value given (see the docs for the accepted values)
            orientation: Choose the images orientation according to the value given (see the docs for the accepted values)
            gif: If False is provided prevent the API to return .gif files, else if True is provided force it to do so
            if nothing (or None) is provided then no filter is applied.
            token: The token that will be use for this request only, this doesn't change the token passed in __init__.
            raw : If True return the raw result.
        Returns:
            A dictionary containing the json the API returned.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(user_id=user_id,
                                     selected_tags=selected_tags,
                                     excluded_tags=excluded_tags,
                                     excluded_files=excluded_files,
                                     is_nsfw=is_nsfw,
                                     many=many,
                                     order_by=order_by,
                                     orientation=orientation,
                                     gif=gif,
                                     )
        headers = self._create_headers(
            **{'User-Agent': self.appname, 'Authorization': f'Bearer {token if token else self.token}'})

        infos = await self._make_request(f"{APIBaseURL}fav/", 'get', params=params, headers=headers)
        if raw:
            return infos
        return [Image(im) for im in infos['images']]

    @requires_token
    async def fav_delete(
            self,
            image: str,
            user_id: str = None,
            token: str = None,
    ) -> Dict:
        """Remove an image from the user gallery.""

        Args:
            image: the file that you want to remove from the gallery.
        Kwargs:
            user_id: The user's id you want to access the gallery (only for trusted apps).
            token: The token that will be use for this request only, this doesn't change the token passed in __init__.
        Returns:
            None
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(user_id=user_id, image=image)
        headers = self._create_headers(
            **{'User-Agent': self.appname, 'Authorization': f'Bearer {token if token else self.token}'})
        return await self._make_request(f"{APIBaseURL}fav/delete/", 'delete', params=params, headers=headers)

    @requires_token
    async def fav_insert(
            self,
            image: str,
            user_id: str = None,
            token: str = None,
    ) -> Dict:
        """Add an image to the user gallery.""
        Args:
            image: the file that you want to add to the gallery.
        Kwargs:
            user_id: The user's id you want to access the gallery (only for trusted apps).
            token: The token that will be use for this request only, this doesn't change the token passed in __init__.
        Returns:
            None
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(user_id=user_id, image=image)
        headers = self._create_headers(
            **{'User-Agent': self.appname, 'Authorization': f'Bearer {token if token else self.token}'})
        return await self._make_request(f"{APIBaseURL}fav/insert/", 'post', params=params, headers=headers)

    @requires_token
    async def fav_toggle(
            self,
            image: str,
            user_id: str = None,
            token: str = None,
    ) -> Dict:
        """Remove or add an image to the user gallery, depending on if it is already in.""

        Kwargs:
            user_id: The user's id you want to access the gallery (only for trusted apps).
            token: The token that will be use for this request only, this doesn't change the token passed in __init__.
        Returns:
            A dictionary containing the json the API returned.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(user_id=user_id, image=image)
        headers = self._create_headers(
            **{'User-Agent': self.appname, 'Authorization': f'Bearer {token if token else self.token}'})
        return await self._make_request(f"{APIBaseURL}fav/toggle/", 'post', params=params, headers=headers)

    async def info(self, images: List[str], raw=False) -> List[Image]:
        """Fetch the images' data (as if you were requesting a gallery containing only those images)
        args:
            images : A list of images filenames to provide.
        Kwargs:
            raw : If True return the raw result.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(images=images)
        headers = self._create_headers(**{'User-Agent': self.appname})
        infos = await self._make_request(f"{APIBaseURL}info/", 'get', params=params, headers=headers)
        if raw:
            return infos
        return [Image(im) for im in infos['images']]

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
        return await self._make_request(f"{APIBaseURL}report/", 'get', params=params, headers=headers)

    async def tags(self) -> List[Tag]:
        """Gets the API endpoints, same as endpoints method but returns a list of Tag (see types.py).
        Returns:
            A list of Tag.
        Raises:
            APIException: If the API response contains an error.
        """
        params = self._create_params(full=True)
        headers = self._create_headers(**{'User-Agent': self.appname})
        results = await self._make_request(APIBaseURL + f'endpoints/', 'get', params=params, headers=headers)
        tags = []
        for k, v in results.items():
            for tag_infos in v:
                tags.append(Tag(tag_infos))
        return tags

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
        return await self._make_request(APIBaseURL + f'endpoints/', 'get', params=params, headers=headers)
