from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('youtube-to-bigquery-493401d956f9.json')
project_id = 'youtube-to-bigquery'
client = bigquery.Client(credentials=credentials, project=project_id)

def load(new_row: dict) -> str:

    columns = ', '.join(new_row.keys())
    values = ', '.join([
        str(value) if isinstance(value, (int, float))
        else f"'{value}'"
        for value in new_row.values()
    ])

    out_query = f"""
    INSERT INTO newonce-178415.content.articles_analytics_1 ({columns})
    VALUES ({values})
    """

    q = client.query(out_query)
    re = q.result()

    result = f'Executed the following query: {out_query} with result: {re}'

    return result