from os import getenv

from polars import DataFrame

import duckdb

_CONNECTION_STRING = getenv("XLR_AZURE_CONNECTION_STRING")


def get_azure_df(path: str, columns: list[str] | None = None) -> DataFrame:
    con = duckdb.connect(database=":memory:")
    select_stmt = "*" if columns is None else ", ".join(columns)
    try:
        con.install_extension("httpfs")
        con.install_extension("azure")
        con.load_extension("httpfs")
        con.load_extension("azure")
        con.sql(
            f"CREATE OR REPLACE SECRET az (TYPE azure, CONNECTION_STRING '{_CONNECTION_STRING}');"
        )
        df = con.sql(f"SELECT {select_stmt} FROM read_parquet('{path}');").pl()
    except Exception as e:
        print(f"Error connecting to Azure: {e}")
        raise e
    finally:
        con.close()
    return df
