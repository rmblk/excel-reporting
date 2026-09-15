from os import getenv
from datetime import date, timedelta

from polars import DataFrame
from xlsxwriter.utility import (
    xl_rowcol_to_cell,
    xl_cell_to_rowcol,
    xl_col_to_name,
    xl_range,
    xl_range_abs,
)

from .util import get_azure_df
from .excel import (
    to_excel_date,
    write_df_to_excel,
    Format,
    Section,
    Worksheet,
    Workbook,
)

TODAY = date.today() - timedelta(days=1)
EXCEL_TODAY = to_excel_date(TODAY)
