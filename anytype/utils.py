import random
import mistune

import anytype.types
import anytype.csvfile
import anytype.markdown


def markdown_from_csv(obj: anytype.csvfile.CSVFile):
    m = anytype.markdown.MarkdownRenderer()
    return m.render([obj.to_ast()])


def csv_from_markdown(markdown_text):
    md = mistune.create_markdown(renderer="ast", plugins=["table"])
    ast = md(markdown_text)
    table_node = next(
        (node for node in ast if node.get("type") == "table"), None
    )
    if table_node is None:
        raise ValueError("В markdown не найдена таблица")
    return anytype.csvfile.CSVFile.from_ast(table_node)


def random_color():
    return random.choice(list(anytype.types.TagColorEnum))


def random_hex6(uppercase=False):
    fmt = "{:06X}" if uppercase else "{:06x}"
    return fmt.format(random.getrandbits(24))


def get_space_id(
    space_query,
    num: int = 0,
) -> str:
    import anytype.queryes  # noqa

    if num >= 0:
        spaces = space_query.get_spaces()
        if not spaces:
            raise RuntimeError("Нет доступных пространств")
        return spaces[num - 1].get("id", "")
    spaces = space_query.get_spaces()
    if not spaces:
        raise RuntimeError("Нет доступных пространств")
    print("\nДоступные пространства:")
    for i, s in enumerate(spaces):
        print(f"{i+1}. {s.get('name')}")
    choice = int(input("Выберите пространство (номер): ")) - 1
    return spaces[choice].get("id", "")


def extract_code_in_markdown(text: str) -> str:
    return text.split("```")[1] if "```" in text else text
