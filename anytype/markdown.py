class MarkdownRenderer:
    def __init__(self):
        self.handlers = {
            "heading": self.render_heading,
            "table": self.render_table,
            "paragraph": self.render_paragraph,
            "blank_line": self.render_blank_line,
        }

    def render(self, ast):
        lines = []
        for node in ast:
            handler = self.handlers.get(node["type"], self.render_unknown)
            block = handler(node)
            if block:
                lines.append(block)
        return "\n".join(lines)

    def render_heading(self, node):
        level = node["attrs"]["level"]
        text = "".join(child["raw"] for child in node["children"])
        return f"{'#' * level} {text}   "

    def render_paragraph(self, node):
        text = "".join(
            child["raw"] if child["type"] == "text" else "\n"
            for child in node["children"]
        )
        return text

    def render_blank_line(self, node):
        return ""

    def render_table(self, node):
        head = node["children"][0]
        body = node["children"][1]
        headers = [
            "".join(ch["raw"] for ch in cell["children"])
            for cell in head["children"]
        ]
        rows = [
            [
                "".join(ch["raw"] for ch in cell["children"])
                for cell in row["children"]
            ]
            for row in body["children"]
        ]
        cols = list(zip(headers, *rows))
        widths = [max(len(x.strip()) for x in col) for col in cols]
        header_line = (
            "| "
            + " | ".join(h.rjust(w) for h, w in zip(headers, widths))
            + " |"
        )
        sep_line = (
            "| " + " | ".join(":" + "-" * (w - 1) for w in widths) + " |"
        )
        body_lines = [
            "| " + " | ".join(c.rjust(w) for c, w in zip(row, widths)) + " |"
            for row in rows
        ]
        return "\n".join([header_line, sep_line, *body_lines])

    def render_unknown(self, node):
        return f"<!-- Unknown node: {node['type']} -->"
