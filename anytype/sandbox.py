from anytype.queryes import (
    QuerySession,
    PageQuery,
    CreateQuery,
    TemplateQuery,
    TypeQuery,
    PropertyQuery,
    TagQuery,
)

PQ = PageQuery
CQ = CreateQuery
TempQ = TemplateQuery
TQ = TypeQuery
PropQ = PropertyQuery
TagQ = TagQuery

def sandbox(
    code: str,
    query_session: QuerySession,
    namespace: dict,
    space_id: str,
) -> None:
    srq = [query_session, space_id]
    exec(code)
