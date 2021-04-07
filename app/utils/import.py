import pandas as pd
from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers


final_columns = ["job_title", "city", "state", "salary"]


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

    # rename column names and replace NaN with ""
    df.columns = final_columns
    df = df.fillna("")

    return df


def get_data():
    """retrieve data from url and ingest into pandas"""
    # url = "H_1B_Disclosure_Data_FY2019-sample.xlsx"  # sample dataset for testing purposes
    url = "https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2019/H-1B_Disclosure_Data_FY2019.xlsx"
    df = pd.read_excel(url)
    return df


def filter_keys(document):
    """ convert pandas dataframe row to dict """
    return {col: document[col] for col in final_columns}


def doc_generator(df):
    """ create generator for es bulk ingestion """
    df_iter = df.iterrows()
    for index, document in df_iter:
        yield {
            "_index": "salary",
            "_source": filter_keys(document),
        }


def main():
    """ entrypoint for import script """
    # get and transform data
    print("Retrieving data from url... it make take up to 10-15+ minutes depending on the available CPU/RAM.")
    data = get_data()
    transformed_data = transform_data(data)
    print(transformed_data.head())

    # init elasticsearch connection
    es_client = Elasticsearch(
        hosts=[{"host": "elasticsearch", "port": 9200}],
        connection_class=RequestsHttpConnection,
        max_retries=30,
        retry_on_timeout=True,
        request_timeout=30,
        http_compress=True,
    )
    # create elasticsearch index
    print("Creating salary index...")
    es_client.indices.create(index='salary', ignore=400)

    # bulk import dataframe into elasticsearch using a generator
    print("Bulk importing rows into Elasticsearch.... Please wait.")
    helpers.bulk(es_client, doc_generator(transformed_data), raise_on_error=False)
    print("Finished!")


if __name__ == "__main__":
    main()
