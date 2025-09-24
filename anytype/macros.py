import anytype.token
import anytype.queryes
import anytype.utils
import anytype.sandbox


def pyrun(arvg: list[str] | None = None) -> None:
    flag = False
    if len(arvg) >= 2:
        flag = True if "--token" in arvg else False
    token = anytype.token.get_token(flag)
    query_session = anytype.queryes.QuerySession(token)
    space_query = anytype.queryes.SpaceQuery(query_session)
    num = 0
    if arvg:
        num = int(arvg[-1])
    space_id = anytype.utils.get_space_id(space_query, num)
    print("start exec", "__main__")
    anytype.sandbox.run_scripts(query_session, space_id, space="__main__")
    print("end exec", "__main__")
