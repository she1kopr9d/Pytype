from anytype.queryes import (
    QuerySession,
    PageQuery,
)


def sandbox(
    code: str,
    query_session: QuerySession,
    namespace: dict,
    space_id: str,
) -> None:
    exec(code)
