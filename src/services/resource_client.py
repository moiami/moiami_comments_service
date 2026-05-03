from uuid import UUID
from http import HTTPStatus

import requests

from src.core.exceptions import ServiceError


class ResourceClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def movie_exists(self, movie_id: UUID) -> bool:
        url = f"{self.base_url}/api/v1/catalog/movies/{movie_id}"

        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 404:
                return False

            if response.status_code != 200:
                raise ServiceError(
                    "Resource service returned error",
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

            parsed = response.json()
            if not isinstance(parsed, dict):
                return False

            returned_id = parsed.get("id")
            if returned_id is None:
                return False

            return str(returned_id) == str(movie_id)
        except requests.Timeout:
            raise ServiceError(
                "Resource service is unavailable",
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            )
        except requests.RequestException:
            raise ServiceError(
                "Resource service returned error",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        except ValueError:
            raise ServiceError(
                "Resource service returned invalid values",
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
