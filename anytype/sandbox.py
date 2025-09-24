from anytype.queryes import (
    QuerySession,
    PageQuery,
)
import anytype.utils


class StopExec(Exception):
    pass


def run_scripts(
    query_session: QuerySession,
    space_id: str = "",
    space: str = "__main__",
    globals: dict | None = None,
) -> None:
    page_query = PageQuery(query_session, space_id)
    data = page_query.get_object_by_type("pyrun")["data"]
    for item in data:
        page = page_query.get_page_by_id(item["id"])
        code = anytype.utils.extract_code_in_markdown(
            page["object"]["markdown"]
        )
        sandbox(code, query_session, space_id, space, globals)


def sandbox(
    code: str,
    query_session: QuerySession,
    space_id: str = "",
    space: str = "__none__",
    globals: dict | None = None,
) -> None:
    globals = globals or {}
    globals.update({
        "query_session": query_session,
        "space_id": space_id,
        "space": space,
        "StopExec": StopExec,
        "run_scripts": run_scripts,
        "PageQuery": PageQuery,
        "QuerySession": QuerySession,
    })
    try:
        exec(code, globals)
    except StopExec:
        pass
