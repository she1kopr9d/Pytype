from anytype.queryes import (
    QuerySession,
    PageQuery,
    CreateQuery,
    TemplateQuery,
    TypeQuery,
    PropertyQuery,
    TagQuery,
)
from anytype.types import (
    TagColorEnum,
)
from anytype.csvfile import (
    CSVFile,
)
from anytype.utils import (
    csv_from_markdown,
    markdown_from_csv,
)
from anytype.markdown import (
    MarkdownRenderer
)

# short cut
PQ = PageQuery
CQ = CreateQuery
TempQ = TemplateQuery
TQ = TypeQuery
PropQ = PropertyQuery
TagQ = TagQuery
Color = TagColorEnum
CSV = CSVFile
get_table = csv_from_markdown
MDR = MarkdownRenderer
md_table = markdown_from_csv


def sandbox(
    code: str,
    query_session: QuerySession,
    namespace: dict,
    space_id: str,
) -> None:
    # space require query
    srq = [query_session, space_id]  # noqa
    exec(code)
