import io
import time

import pandas as pd
import requests


def annualize_salary(row):
    """annualize salary if hourly wage is provided - assumption is made that most hourly wages here are full time. thought it would be better to keep data and have certain assumptions than to destroy data"""
    wage_rate = (
        row["WAGE_RATE_OF_PAY_TO_1"]
        if not pd.isnull(row["WAGE_RATE_OF_PAY_TO_1"])
        else row["WAGE_RATE_OF_PAY_FROM_1"]
    )
    annual_salary = (
        wage_rate * 40 * 52 if row["WAGE_UNIT_OF_PAY_1"] == "Hour" else wage_rate
    )
    return annual_salary


def transform_data(df):
    """clean and transform data"""
    # select desired columns from raw data
    cols = [
        "JOB_TITLE",
        # "FULL_TIME_POSITION",
        "EMPLOYER_CITY",
        "EMPLOYER_STATE",
        "WAGE_UNIT_OF_PAY_1",
        "WAGE_RATE_OF_PAY_TO_1",
        "WAGE_RATE_OF_PAY_FROM_1",
    ]
    df = df.reindex(columns=cols)

    # annualize salary for hourly rate
    df["SALARY"] = df.apply(lambda row: annualize_salary(row), axis=1)

    # remove unnecessary columns
    df.drop(
        ["WAGE_RATE_OF_PAY_TO_1", "WAGE_RATE_OF_PAY_FROM_1", "WAGE_UNIT_OF_PAY_1"],
        axis=1,
        inplace=True,
    )

    # rename columns
    df.columns = ["job_title", "city", "state", "salary"]

    return df


def get_data():
    """retrieve data from url and ingest into pandas"""
    url = "H_1B_Disclosure_Data_FY2019-1.xlsx"
    # url = "https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2019/H-1B_Disclosure_Data_FY2019.xlsx"
    df = pd.read_excel(url)
    return df


def main():
    data = get_data()
    transformed_data = transform_data(data)
    print(transformed_data.head())


if __name__ == "__main__":
    main()
