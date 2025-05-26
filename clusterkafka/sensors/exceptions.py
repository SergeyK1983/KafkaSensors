from aiohttp import ClientResponse
from aiohttp.client_exceptions import ClientResponseError


class SensorsException(Exception):
    pass


class SensorResponseException(SensorsException):

    @staticmethod
    def raise_status_exception(response: ClientResponse, message: str) -> None:
        """
        raises:
            ClientResponseError if status code is not 200 or 201.
        """
        if response.status not in (200, 201):
            raise ClientResponseError(
                request_info=response.request_info,
                history=(response, ),
                status=response.status,
                message=message
            )

