from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta

def get_date_months_ago(months: int):
    today = datetime.today()
    three_months_ago = today - relativedelta(months=months)

    formatted_date = three_months_ago.strftime("%Y%m%d")
    return formatted_date

def get_corporate_code(corp_name: str):
    file_path = "/config/workspace/ChatGPT-plugin-test/plugin/dart/corpcode.json"
    with pd.read_json(file_path, lines=True, chunksize=300) as reader:
        for idx, chunk in enumerate(reader):
            ret = chunk.loc[chunk['corp_name'] == corp_name, "corp_code"]
            if ret.empty:
                continue
            corp_code = ret.item()
            return str(corp_code).rjust(8, '0') 
        return None