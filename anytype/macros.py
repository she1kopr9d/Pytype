import anytype.token
import anytype.queryes
import anytype.utils
import anytype.sandbox


def init_namespace(files: list[str]) -> tuple[dict, list]:
    data = {
        file.split("\n")[0][2:]: file
        for file in files
        if file.split("\n")[0][2:] != "__main__"
    }
    mains = [file for file in files if file.split("\n")[0][2:] == "__main__"]
    return (data, mains)


def replace_include_script(
    script_name: str,
    code: str,
    pragma_once: list,
) -> tuple[str, list]:
    pragma_once.append(script_name)
    lines = code.split("\n")
    new_lines = []
    new_line = None
    for line in lines:
        new_line = line
        if "include " in line:
            link = line.replace("include ", "")
            if link in pragma_once:
                new_line = ""
            else:
                new_line = f'exec(namespace["{link}"])'
                pragma_once.append(link)
        new_lines.append(new_line)
    return ("\n".join(new_lines), pragma_once)


def replace_include(namespace: dict) -> dict:
    pragma_once = ["__main__"]
    for key in namespace.keys():
        namespace[key], pragma_once = replace_include_script(
            key,
            namespace[key],
            pragma_once,
        )
    return namespace


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
    page_query = anytype.queryes.PageQuery(query_session, space_id)
    data = page_query.get_object_by_type("pyrun")["data"]
    scripts = []
    for item in data:
        page = page_query.get_page_by_id(item["id"])
        code = anytype.utils.extract_code_in_markdown(
            page["object"]["markdown"]
        )
        code = code[code.index("#") :]
        scripts.append(code)
    namespace, mains = init_namespace(scripts)
    namespace = replace_include(namespace)
    for main in mains:
        main_code = replace_include_script("__main__", main, [])[0]
        anytype.sandbox.sandbox(
            code=main_code,
            query_session=query_session,
            namespace=namespace,
            space_id=space_id,
        )
