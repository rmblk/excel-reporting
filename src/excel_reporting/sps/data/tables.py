import polars as pl

from ...common import (
    DataFrame,
    Workbook,
    TODAY,
    get_azure_df,
    getenv,
    write_df_to_excel,
)

PATH_ROOT = getenv("BLOB_PATH_ROOT", "")


def dim_store() -> DataFrame:
    stores = get_azure_df(
        f"{PATH_ROOT}DimStore.parquet",
        [
            "StoreId",
            "RegionId",
            "StoreNumber",
            "StoreNumber || ' - ' || StoreName AS Store",
            "StoreEmail",
        ],
    )
    regions = get_azure_df(
        f"{PATH_ROOT}DimRegion.parquet", ["RegionId", "RegionName AS Region"]
    )
    stores = (
        stores.join(regions, on="RegionId", how="left")
        .select(["StoreId", "Region", "StoreNumber", "Store", "StoreEmail"])
        .filter(pl.col("StoreNumber") >= "5200")
        .sort("StoreNumber")
    )
    return stores


def dim_department() -> DataFrame:
    df = get_azure_df(
        f"{PATH_ROOT}DimDepartment.parquet",
        [
            "DepartmentId",
            "GLCode",
            "GLName AS Department",
        ],
    )
    return (
        df.filter((pl.col("DepartmentId").le(9)) | (pl.col("DepartmentId").eq(26)))
        .select(["GLCode", "Department"])
        .sort("GLCode")
    )


def dim_date() -> DataFrame:
    df = (
        get_azure_df(
            f"{PATH_ROOT}DimDate.parquet",
            [
                "DateId",
                "Date",
                "FiscalYear",
                "(Year * 10) + Quarter AS QuarterId",
                "MonthId",
                "WeekId",
                "IsHoliday",
            ],
        )
        .filter(pl.col("DateId").le(int(TODAY.strftime("%Y%m%d"))))
        .with_columns(pl.col("Date").cast(pl.Date))
    )
    today = df.filter(pl.col("DateId").eq(int(TODAY.strftime("%Y%m%d")))).row(0)
    fiscal_year, quarter_id, month_id, week_id = today[2:6]

    return df.with_columns(
        [
            pl.col("FiscalYear").eq(fiscal_year).cast(pl.UInt8).alias("IsCurrentYear"),
            pl.col("QuarterId").eq(quarter_id).cast(pl.UInt8).alias("IsCurrentQuarter"),
            pl.col("MonthId").eq(month_id).cast(pl.UInt8).alias("IsCurrentMonth"),
            pl.col("WeekId").eq(week_id).cast(pl.UInt8).alias("IsCurrentWeek"),
            pl.col("IsHoliday").cast(pl.UInt8).alias("IsHoliday"),
        ]
    ).select(
        [
            "DateId",
            "Date",
            "IsCurrentYear",
            "IsCurrentQuarter",
            "IsCurrentMonth",
            "IsCurrentWeek",
            "IsHoliday",
        ]
    )


def fact_targets() -> DataFrame:
    return get_azure_df(f"{PATH_ROOT}FactTargets.parquet").with_columns(
        pl.col("GLCode").cast(pl.String)
    )


def fact_dept_sales() -> DataFrame:
    sales = get_azure_df(
        f"{PATH_ROOT}FactDeptSales.parquet",
        [
            "StoreId",
            "DateId",
            "GLCode",
            "ItemsSold",
            "DiscountAmount",
            "DiscountCount",
            "Sales",
        ],
    )
    targets = fact_targets()
    dates = dim_date()
    depts = dim_department()
    stores = dim_store()

    return (
        sales.join(targets, on=["StoreId", "DateId", "GLCode"], how="left")
        .with_columns(pl.col("SalesBudget").fill_null(0.0))
        .join(dates, on="DateId", how="inner")
        .join(depts, on="GLCode", how="inner")
        .join(stores, on="StoreId", how="inner")
        .select(
            [
                "StoreNumber",
                "DateId",
                "GLCode",
                "ItemsSold",
                "DiscountAmount",
                "DiscountCount",
                "Sales",
                "SalesBudget",
                "IsCurrentYear",
                "IsCurrentQuarter",
                "IsCurrentMonth",
                "IsCurrentWeek",
                "IsHoliday",
            ]
        )
    )


def fact_dept_prod() -> DataFrame:
    prod = get_azure_df(
        f"{PATH_ROOT}FactDeptProd.parquet",
        [
            "StoreId",
            "DateId",
            "GLCode",
            "ItemsProduced",
            "ProductionValue",
        ],
    )
    targets = fact_targets()
    dates = dim_date()
    depts = dim_department()
    stores = dim_store()

    return (
        prod.join(targets, on=["StoreId", "DateId", "GLCode"], how="left")
        .with_columns(pl.col("ProductionQuota").fill_null(0))
        .join(dates, on="DateId", how="inner")
        .join(depts, on="GLCode", how="inner")
        .join(stores, on="StoreId", how="inner")
        .select(
            [
                "StoreNumber",
                "DateId",
                "GLCode",
                "ItemsProduced",
                "ProductionValue",
                "ProductionQuota",
                "IsCurrentYear",
                "IsCurrentQuarter",
                "IsCurrentMonth",
                "IsCurrentWeek",
                "IsHoliday",
            ]
        )
    )


def load_tables(workbook: Workbook) -> None:
    write_df_to_excel(
        dim_date()
        .filter(pl.col("IsHoliday") == 0)
        .select("Date")
        .sort("Date", descending=True),
        workbook=workbook.workbook,
        worksheet="DimDate",
    )
    write_df_to_excel(
        dim_store(),
        workbook=workbook.workbook,
        worksheet="DimStore",
    )
    write_df_to_excel(
        fact_dept_sales(), workbook=workbook.workbook, worksheet="FactSales"
    )
    write_df_to_excel(
        fact_dept_prod(), workbook=workbook.workbook, worksheet="FactProd"
    )
