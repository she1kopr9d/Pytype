import requests

import anytype


class QuerySession:
    __token: str = ""
    __api_link: str = ""
    __header: str = {}

    def __init__(
        self,
        token: str,
        api_link: str = anytype.API_BASE,
    ) -> None:
        self.__token = token
        self.__api_link = api_link
        self.__header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Authorization": f"Bearer {self.__token}",
            "Anytype-Version": anytype.API_VERSION
        }

    def request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        json: dict = None,
    ) -> dict:
        url = f"{self.__api_link}{endpoint}"
        response = requests.request(
            method,
            url,
            headers=self.__header,
            params=params or {},
            json=json or {},
        )
        response.raise_for_status()
        return response.json()


class BaseQuery():
    __query: QuerySession

    def __init__(self, query: QuerySession) -> None:
        self.__query = query

    def get_query(self) -> QuerySession:
        return self.__query


class SpaceQuery(BaseQuery):

    def __init__(self, query: QuerySession) -> None:
        super().__init__(query)

    def get_spaces(self) -> list[dict]:
        return super().get_query().request("GET", "/spaces").get("data", [])


class PageQuery(BaseQuery):
    __space_id: str

    def __init__(self, query: QuerySession, space_id: str) -> None:
        self.__space_id = space_id
        super().__init__(query)

    def get_pages(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        params = {
            "limit": limit,
            "offset": offset
        }
        payload = {}
        return super().get_query().request(
            "GET",
            f"/spaces/{self.__space_id}/objects",
            params=params,
            json=payload,
        ).get("data", [])

    def get_page_by_id(
        self,
        object_id: str,
    ) -> dict:
        params = {}
        return super().get_query().request(
            "GET",
            f"/spaces/{self.__space_id}/objects/{object_id}",
            params=params,
        )

    def get_object_by_type(
        self,
        type_name: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        params = {
            "limit": limit,
            "offset": offset
        }
        payload = {
            "query": "",
            "sort": {
                "direction": "desc",
            },
            "types": [
                type_name,
            ]
        }
        return super().get_query().request(
            "POST",
            f"/spaces/{self.__space_id}/search",
            params=params,
            json=payload,
        )

    def search_by_tags(
        self,
        limit: int = 50,
        offset: int = 0,
        tag: dict = None,
    ) -> list[dict]:
        params = {
            "limit": limit,
            "offset": offset
        }
        print(tag)
        payload = {
            "query": "",
            "sort": {
                "direction": "desc",
            },
            "types": [
                "Pyruns",
            ]
        }
        return super().get_query().request(
            "POST",
            f"/spaces/{self.__space_id}/search",
            params=params,
            json=payload,
        )


class PropertyQuery(BaseQuery):
    __space_id: str

    def __init__(self, query: QuerySession, space_id: str) -> None:
        self.__space_id = space_id
        super().__init__(query)

    def get_properties(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        params = {}
        return super().get_query().request(
            "GET",
            f"/spaces/{self.__space_id}/properties",
            params=params,
        ).get("data", [])


class TagQuery(BaseQuery):
    __space_id: str

    def __init__(self, query: QuerySession, space_id: str) -> None:
        self.__space_id = space_id
        super().__init__(query)

    def get_tags(
        self,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        params = {}
        return super().get_query().request(
            "GET",
            f"/spaces/{self.__space_id}/properties/bafyreigkzaf2tcacw6uyss7hg7kjg2u5ntujczzk6ycds2kbqtoafy2yam/tags",
            params=params,
        ).get("data", [])
