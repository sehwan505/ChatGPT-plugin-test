import requests
from util import config
import xml.etree.ElementTree as ET
from fastapi import APIRouter
from datetime import datetime
from dateutil.relativedelta import relativedelta

api_key = config["DART_KEY"]

router = APIRouter(
    prefix="/dart",
)

@router.get("/get_dart_disclosure_by_corporate")
def get_dart_disclosure_by_corporate(corp_name: str):
    corp_code = get_corporate_code(corp_name)
    if corp_code == None:
        return "해당 기업이 없습니다"
    else:
        print(corp_code)
        corp_code = str(corp_code).rjust(8, '0')

    url = 'https://opendart.fss.or.kr/api/list.json'  # replace with the actual endpoint
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': get_date_months_ago(9),
        'pblntf_ty': 'A' # 정기 공시
    }

    print(params)
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None

import pandas as pd

@router.get("/get_corporate_code")
def get_corporate_code(corp_name: str):
    file_path = "/config/workspace/ChatGPT-plugin-test/plugin/dart/corpcode.json"
    with pd.read_json(file_path, lines=True, chunksize=300) as reader:
        for idx, chunk in enumerate(reader):
            ret = chunk.loc[chunk['corp_name'] == corp_name, "corp_code"]
            if ret.empty:
                continue
            return ret.item()
        return None


def get_date_months_ago(months: int):
    today = datetime.today()
    three_months_ago = today - relativedelta(months=months)

    formatted_date = three_months_ago.strftime("%Y%m%d")
    return formatted_date