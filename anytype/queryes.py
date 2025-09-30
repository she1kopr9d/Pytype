import requests

import anytype
import anytype.builder
import anytype.utils
import anytype.types


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
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {self.__token}",
            "Anytype-Version": anytype.API_VERSION,
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


class BaseQuery:
    __query: QuerySession

    def __init__(self, query: QuerySession) -> None:
        self.__query = query

    def get_query(self) -> QuerySession:
        return self.__query


class SpaceRequireQuery(BaseQuery):
    __space_id: str

    @property
    def space_id(self):
        return self.__space_id

    def __init__(self, query: QuerySession, space_id: str):
        self.__space_id = space_id
        super().__init__(query)


class SpaceQuery(BaseQuery):

    def __init__(self, query: QuerySession) -> None:
        super().__init__(query)

    def get_spaces(self) -> list[dict]:
        return super().get_query().request("GET", "/spaces").get("data", [])


class PageQuery(SpaceRequireQuery):
    def get_pages(
        self,
        limit: int = 100,
        offset: int = 0,
    ) -> list[dict]:
        params = {"limit": limit, "offset": offset}
        payload = {}
        return (
            super()
            .get_query()
            .request(
                "GET",
                f"/spaces/{super().space_id}/objects",
                params=params,
                json=payload,
            )
            .get("data", [])
        )

    def get_page_by_id(
        self,
        object_id: str,
    ) -> dict:
        params = {}
        return (
            super()
            .get_query()
            .request(
                "GET",
                f"/spaces/{super().space_id}/objects/{object_id}",
                params=params,
            )
        )

    def get_object_by_type(
        self,
        type_name: str,
        limit: int = 50,
        offset: int = 0,
    ) -> list[dict]:
        params = {"limit": limit, "offset": offset}
        payload = {
            "query": "",
            "sort": {
                "direction": "desc",
            },
            "types": [
                type_name,
            ],
        }
        return (
            super()
            .get_query()
            .request(
                "POST",
                f"/spaces/{super().space_id}/search",
                params=params,
                json=payload,
            )
        )

    def get_by_name(
        self, name: str, offset: int = 0, is_full: bool = False
    ) -> dict | None:
        objects = self.get_pages(offset=offset)
        if len(objects) == 0:
            return None
        for obj in objects:
            if obj["name"] == name:
                return obj if not is_full else self.get_page_by_id(obj["id"])
        return self.get_by_name(name, offset + 1)

    def get_by_name_more(
        self,
        names: list[str],
        offset: int = 0,
        is_full: bool = False,
        buffer: list[dict] = None,
    ) -> list:
        if buffer is None:
            buffer = []
        objects = self.get_pages(offset=offset)
        if len(objects) == 0:
            return buffer
        for obj in objects:
            if any([obj["name"] == name for name in names]):
                buffer.append(
                    obj if not is_full else self.get_page_by_id(obj["id"])
                )
                names.remove(obj["name"])
                if len(names) == 0:
                    return buffer
        return self.get_by_name_more(
            names=names,
            offset=offset + 1,
            is_full=is_full,
            buffer=buffer,
        )


class TypeQuery(SpaceRequireQuery):
    def get_all(self) -> dict:
        return (
            super()
            .get_query()
            .request(
                "GET",
                f"/spaces/{self.space_id}/types/",
            )
        )


class PropertyQuery(SpaceRequireQuery):
    def get_all(self) -> dict:
        return (
            super()
            .get_query()
            .request(
                "GET",
                f"/spaces/{self.space_id}/properties/",
            )
        )

    def get_id_by_name(self, name: str) -> str:
        return [
            prop["id"]
            for prop in self.get_all()["data"]
            if prop["name"] == name
        ][0]


class TagQuery(SpaceRequireQuery):
    def get_tag_prop_id(self) -> str:
        prop_query = PropertyQuery(
            query=self.get_query(),
            space_id=self.space_id,
        )
        return prop_query.get_id_by_name("Tag")

    def get_all(self, prop_id: str | None = None) -> dict:
        if prop_id is None:
            prop_id = self.get_tag_prop_id()
        return (
            super()
            .get_query()
            .request(
                "GET",
                f"/spaces/{self.space_id}/properties/{prop_id}/tags",
            )
        )

    def get_ids_by_names(
        self, names: list[str], prop_id: str | None = None
    ) -> list[str]:
        tags_id = []
        tags = self.get_all(prop_id=prop_id)["data"]
        for name in names:
            f = False
            for tag in tags:
                if name == tag["name"]:
                    tags_id.append(tag["id"])
                    f = True
            if not f:
                tags_id.append(
                    self.create(name, prop_id=prop_id)["tag"]["id"]
                )
        return [
            tag["id"]
            for tag in self.get_all(prop_id=prop_id)["data"]
            if any([tag["name"] == name for name in names])
        ]

    def create(
        self,
        tag_name: str,
        tag_color: anytype.types.TagColorEnum | None = None,
        prop_id: str | None = None,
    ) -> dict:
        if tag_color is None:
            tag_color = anytype.utils.random_color()
        if prop_id is None:
            prop_id = self.get_tag_prop_id()
        data = {
            "color": tag_color.value,
            "name": tag_name,
        }
        return self.get_query().request(
            "POST",
            f"/spaces/{self.space_id}/properties/{prop_id}/tags",
            json=data,
        )

    def delete(
        self,
        tag_name: str | None = None,
        tag_id: str | None = None,
        prop_id: str | None = None,
    ) -> dict:
        if prop_id is None:
            prop_id = self.get_tag_prop_id()
        if tag_id is None:
            tag_id = self.get_ids_by_names(names=[tag_name], prop_id=prop_id)[
                0
            ]
        return self.get_query().request(
            "DELETE",
            f"/spaces/{self.space_id}/properties/{prop_id}/tags/{tag_id}",
        )


class TemplateQuery(SpaceRequireQuery):
    def get_id_by_name(self, name: str) -> str:
        type_query = TypeQuery(super().get_query(), self.space_id)
        return [
            obj["id"]
            for obj in type_query.get_all()["data"]
            if obj["name"] == name
        ][0]

    def get_all_for_type(
        self,
        type_id: str | None = None,
        type_name: str | None = None,
    ) -> dict:
        if type_id is None:
            type_id = self.get_id_by_name(type_name)
        return (
            super()
            .get_query()
            .request(
                "GET",
                f"/spaces/{self.space_id}/types/{type_id}/templates",
            )
        )

    def get_by_name(
        self,
        template_name: str,
        type_id: str | None = None,
        type_name: str | None = None,
        templates: list | None = None,
    ):
        if templates is None:
            templates = self.get_all_for_type(
                type_id=type_id,
                type_name=type_name,
            )
        return [
            temp for temp in templates["data"] if temp["name"] == template_name
        ][0]


class CreateQuery(SpaceRequireQuery):
    def create(
        self,
        body: str = "",
        emoji: str = "📄",
        name: str = "file",
        description: str = "",
        height: int = 42,
        tag_ids: list[str] | None = None,
        tag_names: list[str] | None = None,
        template_id: str | None = None,
        template_name: str | None = None,
        type_key: str = "page",
        type_name: str = "Page",
    ):
        if template_name is not None:
            temp_query = TemplateQuery(self.get_query(), self.space_id)
            template_id = temp_query.get_by_name(
                template_name=template_name,
                type_name=type_name,
            )["id"]
        if tag_names is not None:
            tag_query = TagQuery(self.get_query(), self.space_id)
            tag_ids = tag_query.get_ids_by_names(names=tag_names)
        data = anytype.builder.create_object(
            body=body,
            emoji=emoji,
            name=name,
            description=description,
            type_key=type_key,
            tag_ids=tag_ids,
            template_id=template_id,
        )
        return (
            super()
            .get_query()
            .request(
                "POST",
                f"/spaces/{super().space_id}/objects",
                json=data,
            )
        )
