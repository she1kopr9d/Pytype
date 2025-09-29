import ast
import tabulate


class CSVFile:
    _table: list
    _headers: tuple
    _types: list

    @property
    def types(self) -> list:
        return self._types

    def __init__(self, *args, types, items=None):
        self._headers = args
        self._types = types
        self._table = list() if items is None else items

    @classmethod
    def from_ast(cls, ast_table, types=None):
        headers = [
            cell["children"][0]["raw"]
            for cell in ast_table["children"][0]["children"]
        ]
        rows = []
        for row in ast_table["children"][1]["children"]:
            values = [cell["children"][0]["raw"] for cell in row["children"]]
            rows.append(values)
        if types is None:
            types = []
            for col in zip(*rows):
                try:
                    test_values = [
                        ast.literal_eval(v.replace(",", ".")) for v in col
                    ]
                    types.append(type(test_values[0]))
                except Exception:
                    types.append(str)
            typed_rows = []
            for row in rows:
                typed_row = {}
                for h, t, v in zip(headers, types, row):
                    v_str = v.strip()
                    if t in (float, int):
                        v_clean = v_str.replace(",", ".")
                        try:
                            num = float(v_clean)
                            if t is int and num.is_integer():
                                num = int(num)
                            typed_row[h] = num
                        except ValueError:
                            typed_row[h] = v_str
                    else:
                        typed_row[h] = v_str
                typed_rows.append(typed_row)
        else:
            typed_rows = [
                {h: t(v) for h, t, v in zip(headers, types, row)}
                for row in rows
            ]
        return cls(*headers, types=types, items=typed_rows)

    def __str__(self) -> str:
        if not self._headers or not self._table:
            return ""
        table_data = []
        for item in self._table:
            row = [item[header] for header in self._headers]
            table_data.append(row)
        return tabulate.tabulate(
            table_data,
            headers=self._headers,
            tablefmt="grid",
            stralign="left",
            numalign="right",
            showindex=False,
            missingval="",
            disable_numparse=False,
        )

    def add_item(self, *args) -> None:
        if len(args) != len(self._headers):
            raise ValueError(
                "Неверное количество аргументов: "
                f"ожидалось {len(self._headers)}, "
                f"получено {len(args)}"
            )

        try:
            item = {
                key: transform(value)
                for key, transform, value in zip(
                    self._headers, self._types, args
                )
            }
            self._table.append(item)
        except Exception as e:
            raise ValueError(f"Ошибка преобразования данных: {e}") from e

    def query(self, *args):
        if len(args) == 0:
            return self
        query_obj = Query_CSVFile(*self._headers, types=self._types)
        for item in self._table:
            if all([filter(item) for filter in args]):
                query_obj.add_item(item)
        return query_obj

    def get_column(self, column):
        return [item[column] for item in self._table]

    def avg(self, column):
        for col, col_type in zip(self._headers, self._types):
            if col == column and col_type is str:
                raise TypeError("Невозможно просчитать avg у str типа")
        cells = self.get_column(column)
        if not cells:
            raise ZeroDivisionError(
                "Невозможно вычислить среднее для пустой таблицы"
            )
        return sum(cells) / len(cells)

    def min(self, column):
        cells = self.get_column(column)
        if not cells:
            raise ValueError("Невозможно вычислить min для пустой таблицы")
        return min(cells)

    def max(self, column):
        cells = self.get_column(column)
        if not cells:
            raise ValueError("Невозможно вычислить max для пустой таблицы")
        return max(cells)

    def to_ast(self):
        return {
            "type": "table",
            "children": [
                {
                    "type": "table_head",
                    "children": [
                        {
                            "type": "table_cell",
                            "attrs": {"align": "left", "head": True},
                            "children": [{"type": "text", "raw": h}],
                        }
                        for h in self._headers
                    ],
                },
                {
                    "type": "table_body",
                    "children": [
                        {
                            "type": "table_row",
                            "children": [
                                {
                                    "type": "table_cell",
                                    "attrs": {"align": "left", "head": False},
                                    "children": [
                                        {"type": "text", "raw": str(item[h])}
                                    ],
                                }
                                for h in self._headers
                            ],
                        }
                        for item in self._table
                    ],
                },
            ],
        }


class Query_CSVFile(CSVFile):
    def add_item(self, item) -> None:
        self._table.append(item)

    def to_csv(self) -> CSVFile:
        return CSVFile(
            *self._headers,
            types=self._types,
            items=self._table,
        )
