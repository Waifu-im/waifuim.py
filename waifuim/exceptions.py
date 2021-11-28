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

class WaifuException(Exception):
    """Base exception class for the wrapper."""

class APIException(WaifuException):
    """Exception due to an error response from waifu.im API."""
    def __init__(self, status : int, message : str) -> None:
        """Initializes the APIException.
        Args:
            status: HTTP status code of the response.
            message: The response message.
        """
        super().__init__(f'{status}: {message}')
        self.status=status
        self.message=message
        

class NoToken(WaifuException):
    """Exception raised when the user try to request the gallery route with no token"""
    def __init__(self, message = f'You tried to request the gallery route with no token. Please pass your token to WaifuAioClient'):
        super().__init__(message)
        self.message = message
        
