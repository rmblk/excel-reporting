from ..common import (
    DataFrame,
    Workbook,
    TODAY,
    EXCEL_TODAY,
    get_azure_df,
    getenv,
    write_df_to_excel,
)
from .data import load_tables


def build():
    workbook = Workbook()
    temp_ws = workbook.workbook.add_worksheet("temp")
    load_tables(workbook)

    workbook.close()
    return workbook.bytes
