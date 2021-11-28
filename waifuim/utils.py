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

from .exceptions import NoToken

APIBaseURL="https://api.waifu.im/" # this can be placed in the aioclient.py itself

def requires_token(func):
    """A decorator used to check if the user passed a token before trying to use the fav method."""
    def wrapper(*args, **kwargs):

        if kwargs.get("token") or args[0].token:

            return func(*args, **kwargs)

        raise NoToken(*('You tried to request the gallery route with no token.', 
                        'Please pass your token to WaifuAioClient')) 
                        # test this out and see im not super sure
                        # this might work?, prolly will

    return wrapper