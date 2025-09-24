import os
import anytype


def get_token(flag: bool = False) -> str:
    if flag and os.path.exists(anytype.TOKEN_FILE):
        with open(anytype.TOKEN_FILE, "r") as f:
            return f.read().strip()
    if os.path.exists(anytype.TOKEN_FILE):
        with open(anytype.TOKEN_FILE, "r") as f:
            token = f.read().strip()
        use_saved = input(
            f"Использовать сохранённый токен? {token[:5]}... (y/n): "
        ).lower()
        if use_saved == "y":
            return token
    token = input("Введите API-токен Anytype: ").strip()
    with open(anytype.TOKEN_FILE, "w") as f:
        f.write(token)
    return token
