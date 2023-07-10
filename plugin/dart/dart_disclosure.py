import requests
from util import config
import xml.etree.ElementTree as ET
import lxml.etree as etree
from fastapi import APIRouter
import pandas as pd
import zipfile
import io
import json
import os
from collections import defaultdict
from .dart_util import get_date_months_ago, get_corporate_code, etree_to_text_list, convert_etree_to_text



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

def save_disclosure_detail(rcept_no: str):
    if os.path.isfile(f"{rcept_no}.xml"):
        print("this file is already exist.")
        return 200
    # return f"https://dart.fss.or.kr/dsaf001/main.do?rcpNo={rcept_no}"
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
    if response.status_code == 200:
        return response.status_code
    else:
        return None

@router.get("/get_contents_of_business")
def get_contents_of_business(rcept_no):
    save_disclosure_detail(rcept_no)
    with open(f"{rcept_no}.xml", 'r') as file:
        content = file.read()
    
    pattern = r"""(<SECTION-1 ACLASS="MANDATORY" APARTSOURCE="SOURCE">\n<TITLE ATOC="Y" AASSOCNOTE="D-0-2-0-0">II\. 사업의 내용<\/TITLE>[\s\S]*?<\/SECTION-1>)"""
    output_str = re.findall(pattern, content)[0]
    tree = ET.ElementTree(ET.fromstring(output_str))
    root = tree.getroot()
    data = convert_etree_to_text(root)
    return data

@router.get("/get_contents_of_management_diagnosis")
def get_contents_of_management_diagnosis(rcept_no):
    save_disclosure_detail(rcept_no)
    with open(f"{rcept_no}.xml", 'r') as file:
        content = file.read()
    
    pattern = r"""(<SECTION-1 ACLASS="MANDATORY" APARTSOURCE="SOURCE">\n<TITLE ATOC="Y" AASSOCNOTE="D-0-4-0-0">IV. 이사의 경영진단 및 분석의견</TITLE>[\s\S]*?<\/SECTION-1>)"""
    output_str = re.findall(pattern, content)[0]
    tree = ET.ElementTree(ET.fromstring(output_str))
    root = tree.getroot()
    data = convert_etree_to_text(root)
    return data

@router.get("/get_contents_of_investor_protection")
def get_contents_of_investor_protection(rcept_no):
    save_disclosure_detail(rcept_no)
    with open(f"{rcept_no}.xml", 'r') as file:
        content = file.read()
    
    pattern = r"""(<SECTION-1 ACLASS="MANDATORY" APARTSOURCE="SOURCE">\n<TITLE ATOC="Y" AASSOCNOTE="D-0-11-0-0">XI. 그 밖에 투자자 보호를 위하여 필요한 사항</TITLE>[\s\S]*?<\/SECTION-1>)"""
    output_str = re.findall(pattern, content)[0]
    tree = ET.ElementTree(ET.fromstring(output_str))
    root = tree.getroot()
    data = convert_etree_to_text(root)
    return data

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
    # pattern3 = r"""(<SECTION-1 ACLASS="MANDATORY" APARTSOURCE="SOURCE">\n<TITLE ATOC="Y" AASSOCNOTE="D-0-2-0-0">II\. 사업의 내용<\/TITLE>[\s\S]*?<\/SECTION-1>)"""
    # output_str3 = re.findall(pattern3, output_str2)

    with open(f"{rcept_no}.xml", 'w') as file:
        file.write(output_str2)
