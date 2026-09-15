from io import BytesIO
from typing import Any
from os import PathLike
from datetime import datetime
from collections.abc import Mapping

from xlsxwriter import Workbook as _Workbook
from xlsxwriter.worksheet import Worksheet as _Worksheet
from xlsxwriter.format import Format as _Format


class Format(Mapping[str, str | int | float | bool | None]):
    def __init__(
        self, format: Mapping[str, str | int | float | bool | None] | None = None
    ) -> None:
        self._format = dict(format or {})

    def __iter__(self):
        return iter(self._format)

    def __len__(self) -> int:
        return len(self._format)

    def __getitem__(self, key: str) -> str | int | float | bool | None:
        return self._format[key]

    def __hash__(self) -> int:  # type: ignore
        return hash(tuple(sorted(self.items())))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Mapping):
            return NotImplemented
        return dict(self) == dict(other)


class _FormatRegistry:
    def __init__(self, workbook: _Workbook) -> None:
        self.workbook = workbook
        self.objects: dict[int, _Format] = {}

    def register(self, format: Format | None) -> _Format | None:
        if format is None:
            return None
        format_hash = hash(format)
        if format_hash not in self.objects:
            self.objects[format_hash] = self.workbook.add_format(dict(format))
        return self.objects[format_hash]


class Section:
    def __init__(self) -> None:
        self._cells: dict[tuple[int, int], tuple[Any, Format | None]] = {}
        self._merged_ranges: list[tuple[int, int, int, int, Any, Format | None]] = []
        self.shape: tuple[int, int] = (0, 0)

    def write(
        self, row: int, col: int, value: Any, format: Format | None = None
    ) -> None:
        self._cells[(row, col)] = (value, format)
        self.shape = (max(self.shape[0], row + 1), max(self.shape[1], col + 1))

    def get_cell(self, row: int, col: int) -> tuple[Any, Format | None] | None:
        return self._cells.get((row, col))

    def write_format(self, row: int, col: int, format: Format | None = None) -> None:
        if self.get_cell(row, col):
            value, _ = self.get_cell(row, col)  # type: ignore
        else:
            value = None
        self._cells[(row, col)] = (value, format)
        self.shape = (max(self.shape[0], row + 1), max(self.shape[1], col + 1))

    def write_value(self, row: int, col: int, value: Any) -> None:
        if self.get_cell(row, col):
            _, format = self.get_cell(row, col)  # type: ignore
        else:
            format = None
        self._cells[(row, col)] = (value, format)
        self.shape = (max(self.shape[0], row + 1), max(self.shape[1], col + 1))

    def merge_range(
        self,
        first_row: int,
        first_col: int,
        last_row: int,
        last_col: int,
        value: Any,
        format: Format | None = None,
    ) -> None:
        self._merged_ranges.append(
            (first_row, first_col, last_row, last_col, value, format)
        )
        self.shape = (
            max(self.shape[0], last_row + 1),
            max(self.shape[1], last_col + 1),
        )

    def get_cells(
        self, row: int = 0, col: int = 0
    ) -> dict[tuple[int, int], tuple[Any, Format | None]]:
        if row < 0 or col < 0:
            raise ValueError("Row and column indices must be non-negative.")
        if row == 0 and col == 0:
            return self._cells

        return {
            (r + row, c + col): (value, format)
            for (r, c), (value, format) in self._cells.items()
        }

    def get_merged_ranges(
        self, row: int = 0, col: int = 0
    ) -> list[tuple[int, int, int, int, Any, Format | None]]:
        if row < 0 or col < 0:
            raise ValueError("Row and column indices must be non-negative.")

        return [
            (
                first_row + row,
                first_col + col,
                last_row + row,
                last_col + col,
                value,
                format,
            )
            for first_row, first_col, last_row, last_col, value, format in self._merged_ranges
        ]


class Worksheet(Section):
    def __init__(self) -> None:
        super().__init__()
        self._rows: dict[int, int] = {}
        self._cols: dict[int, int] = {}

    def set_row_pixels(self, row: int, pixels: int) -> None:
        self._rows[row] = pixels

    def set_col_pixels(self, col: int, pixels: int) -> None:
        self._cols[col] = pixels

    def add_section(
        self, section: Section, start_row: int = 0, start_col: int = 0
    ) -> None:
        for (r, c), (value, format) in section.get_cells(start_row, start_col).items():
            self.write(r, c, value, format)
        for (
            first_row,
            first_col,
            last_row,
            last_col,
            value,
            format,
        ) in section.get_merged_ranges(start_row, start_col):
            self.merge_range(first_row, first_col, last_row, last_col, value, format)


class Workbook:
    def __init__(
        self,
        filename: str | PathLike | None = None,
        options: dict[str, Any] | None = None,
    ) -> None:
        filename = filename or "book.xlsx"
        options = options or {}

        if filename and not isinstance(filename, (str, PathLike)):
            raise TypeError(
                f"filename must be str or PathLike, not {type(filename).__name__}"
            )

        if options and not isinstance(options, dict):
            raise TypeError(f"options must be dict, not {type(options).__name__}")

        options["in_memory"] = True

        self._buffer = BytesIO()
        self.last_flushed: datetime | None = None
        self.data: bytes | None = None
        self.workbook = _Workbook(self._buffer, options)
        self.registry = _FormatRegistry(self.workbook)
        self.worksheets: dict[str, Worksheet] = {}

    def add_worksheet(self, name: str | None = None) -> Worksheet:
        wrapper = Worksheet()
        self.worksheets[name or f"Sheet{len(self.worksheets)}"] = wrapper
        return wrapper

    def flush(self) -> None:
        for name, wrapper in self.worksheets.items():
            worksheet = self.workbook.add_worksheet(name)
            for (
                first_row,
                first_col,
                last_row,
                last_col,
                value,
                format,
            ) in wrapper.get_merged_ranges():
                xlsx_format = self.registry.register(format)
                worksheet.merge_range(
                    first_row,
                    first_col,
                    last_row,
                    last_col,
                    value,
                    xlsx_format,
                )

            cells_dict = wrapper.get_cells()
            cell_keys = [key for key in wrapper.get_cells().keys()]
            cell_keys.sort()
            for row, col in cell_keys:
                value, format = cells_dict[(row, col)]
                xlsx_format = self.registry.register(format)
                worksheet.write(row, col, value, xlsx_format)

            for row, pixels in wrapper._rows.items():
                worksheet.set_row_pixels(row, pixels)

            for col, pixels in wrapper._cols.items():
                worksheet.set_column_pixels(col, col, pixels)  # Convert pixels to width
        self.last_flushed = datetime.now()

    def close(self) -> None:
        if self.last_flushed is None:
            self.flush()
        self.workbook.close()
        self.data = self._buffer.getvalue()
        self._buffer.close()

    @property
    def bytes(self) -> bytes:
        if self.data is None:
            raise ValueError("Workbook has not been closed yet.")
        return self.data
