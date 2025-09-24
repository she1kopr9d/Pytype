import anytype.queryes


def get_space_id(
    space_query: anytype.queryes.SpaceQuery,
    num: int = 0,
) -> str:
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
