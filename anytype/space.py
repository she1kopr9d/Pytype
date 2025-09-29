import requests
import anytype


def get_spaces(token):
    headers = {
        "Authorization": f"Bearer {token}",
        "Anytype-Version": anytype.API_VERSION,
    }
    resp = requests.get(f"{anytype.API_BASE}/spaces", headers=headers)
    resp.raise_for_status()
    return resp.json().get("data", [])


def choose_space():
    spaces = get_spaces()
    if not spaces:
        raise RuntimeError("Нет доступных пространств")
    print("\nДоступные пространства:")
    for i, s in enumerate(spaces):
        print(f"{i+1}. {s.get('name')}")
    choice = int(input("Выберите пространство (номер): ")) - 1
    return spaces[choice]
