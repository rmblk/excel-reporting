from datetime import date

from polars import DataFrame
from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet


def to_excel_date(dt: date) -> int:
    excel_start_date = date(1899, 12, 30)
    delta = dt - excel_start_date
    return delta.days


def write_df_to_excel(
    df: DataFrame,
    workbook: Workbook,
    worksheet: Worksheet | str,
    table_name: str | None = None,
) -> None:
    if table_name is None:
        if type(worksheet) is str:
            _table_name = worksheet
        else:
            _table_name = worksheet.get_name()  # type: ignore
    else:
        _table_name = table_name

    ws = (
        worksheet
        if isinstance(worksheet, Worksheet)
        else workbook.add_worksheet(worksheet)
    )
    df.write_excel(
        workbook=workbook,
        worksheet=ws,
        table_name=_table_name,
    )
    ws.hide()
