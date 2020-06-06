from requests import Response


class NuException(Exception):

    def __init__(self, message):
        super().__init__(message)


class NuRequestException(NuException):
    def __init__(self, response: Response):
        super().__init__(f'The request made failed with HTTP status code {response.status_code}')
        self.url = response.url
        self.status_code = response.status_code
        self.response = response
