import requests
from util import config
import xml.etree.ElementTree as ET
import lxml.etree as etree
from fastapi import APIRouter
import pandas as pd
import zipfile
import io
import json
from .dart_util import get_date_months_ago, get_corporate_code



api_key = config["DART_KEY"]

router = APIRouter(
    prefix="/dart",
)

@router.get("/get_disclosure_list_by_corporate")
def get_disclosure_list_by_corporate(corp_name: str):
    corp_code = get_corporate_code(corp_name)
    if corp_code == None:
        return "해당 기업이 없습니다"
        
    url = 'https://opendart.fss.or.kr/api/list.json'  # replace with the actual endpoint
    params = {
        'crtfc_key': api_key,
        'corp_code': corp_code,
        'bgn_de': get_date_months_ago(9),
        'pblntf_ty': 'A' # 정기 공시
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


@router.get("/get_disclosure_detail")
def get_disclosure_detail(rcept_no: str):
    return f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"
    url = 'https://opendart.fss.or.kr/api/document.xml'  # replace with the actual endpoint
    params = {
        'crtfc_key': api_key,
        'rcept_no': rcept_no
    }

    response = requests.get(url, params=params)
    with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
        # Extract the XML file from the ZIP archive
        zip_ref.extract(f"{rcept_no}.xml")
        replace_reserved_word(rcept_no)
        tree = ET.parse(f"{rcept_no}.xml")
        root = tree.getroot()
    d = etree_to_dict(root)
    if response.status_code == 200:
        return json.dumps(d, indent=4,  ensure_ascii=False)
    else:
        return None


import re
def replace_reserved_word(rcept_no: str):
    with open(f"{rcept_no}.xml", 'r') as file:
        content = file.read()

    pattern = r'(<TE.*?>|<TD.*?>|<P.*?>|<SPAN.*?>)(.*?)(</TE>|</TD>|</P>|</SPAN>)(.*)'
    replacement = r'\1<![CDATA[\2]]>\3<![CDATA[\4]]>'
    output_str = re.sub(pattern, replacement, content)
    pattern2 = r'(<P.*?>)(.*)(\n?<SPAN.*?>)(.*?)(</SPAN>)(.*)'
    replacement2 = r'\1<![CDATA[\2]]>\3\4\5\6'
    output_str2 = re.sub(pattern2, replacement2, output_str)
    # pattern2 = r'<P>(<SPAN>.*?</SPAN>)+(.*?)</P>'
    # replacement2 = r'<P>\1<![CDATA[\2]]></P>'
    # output_str = re.sub(pattern2, replacement2, output_str)
    
    with open(f"{rcept_no}.xml", 'w') as file:
        file.write(output_str2)

def etree_to_dict(t):
    children = list(t)
    if children:
        dd = []
        for dc in map(etree_to_dict, children):
            if isinstance(dc, list):
                dd.extend(dc)
            else:
                dd.append(dc)
        return dd
    else:
        return t.text.strip() if t.text else None
