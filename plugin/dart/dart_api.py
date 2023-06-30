import requests
from util import config
import xml.etree.ElementTree as ET
from fastapi import APIRouter
from io import StringIO

api_key = config["DART_KEY"]

router = APIRouter(
    prefix="/dart",
)

@router.get("/get_dart_disclosure_by_corporate")
def get_dart_disclosure_by_corporate():
    url = 'https://opendart.fss.or.kr/api/list.json'  # replace with the actual endpoint
    params = {
        'crtfc_key': api_key,
        # add other necessary parameters here
    }

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
            ret = chunk.loc[chunk['corp_name'].str.contains(corp_name), "corp_code"]
            if ret.empty:
                continue
            return ret.item()
        return None
