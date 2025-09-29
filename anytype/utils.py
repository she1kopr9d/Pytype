import random

import anytype.types


def random_color():
    return random.choice(list(anytype.types.TagColorEnum))


def random_hex6(uppercase=False):
    fmt = "{:06X}" if uppercase else "{:06x}"
    return fmt.format(random.getrandbits(24))


def get_space_id(
    space_query,
    num: int = 0,
) -> str:
    import anytype.queryes # noqa
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
