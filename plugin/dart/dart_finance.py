import requests
from util import config
from fastapi import APIRouter
import pandas as pd
import json
from .dart_util import get_date_months_ago, get_corporate_code, etree_to_text_list, convert_etree_to_text

api_key = config["DART_KEY"]

router = APIRouter(
    prefix="/dart",
)

@router.get("/financial_statement")
def financial_statement(corp_name: str, year: str, quater: int):
    corp_name = corp_name.replace(" ", "")
    reprt_code = ["11013", "11012", "11014", "11011"]
    url = 'https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json'
    if corp_code := get_corporate_code(corp_name) == None:
        return "회사를 찾을 수 없니다."

    params = {
    'crtfc_key': api_key,
    'corp_code': get_corporate_code(corp_name),
    'bsns_year': year,
    'reprt_code': reprt_code[quater - 1],
    'fs_div': "OFS"
    }
    print(params)
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json().get('list')
        print(data)
        # ret = [{"bsns_year": d["bsns_year"], "account_nm":d["account_nm"], "thstrm_amount": d["thstrm_amount"], "thstrm_add_amount":d["thstrm_add_amount"], "frmtrm_q_amount": d["frmtrm_q_amount"], "frmtrm_add_amount": d["frmtrm_add_amount"]} for d in data]
        return data
    else:
        print(f"Request failed with status code {response.status_code}")
