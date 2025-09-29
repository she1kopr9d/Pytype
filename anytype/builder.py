def create_object(
    body: str = "",
    emoji: str = "📄",
    name: str = "file",
    description: str = "",
    height: int = 42,
    tag_ids: list[str] | None = None,
    template_id: str = None,
    type_key: str = "page",
) -> None:
    properties = [
        {
            "key": "description",
            "text": description,
        },
        {
            "date": "2025-02-14T12:34:56Z",
            "key": "last_modified_date",
        },
    ]
    if tag_ids is not None:
        properties.append(
            {
                "key": "tag",
                "multi_select": tag_ids,
            }
        )
    return {
        "body": body,
        "icon": {"emoji": emoji, "format": "emoji"},
        "name": name,
        "properties": properties,
        "template_id": template_id,
        "type_key": type_key,
    }
