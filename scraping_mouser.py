################################################################################
# 스크래핑 - mouser.kr
################################################################################

import os, sys, traceback
from datetime import datetime
import fire
import pandas as pd
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup

OUTPUT_DIR = 'output'
HISTORY_DIR = 'history'
WORK_NAME = 'mouser'

LIST_FILE_SEP = ' '
HISTORY_FILE_SEP = '\t'
STATUS_CODE_SUCCESS = 200
CONTENT_LENGTH_MIN = 2000

def get_current_time_str():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def extract_texts(page):
    soup = BeautifulSoup(page.content, 'html.parser')

    # 부품 번호
    part_number = soup.find(id='spnManufacturerPartNumber')
    if part_number:
        part_number_text = part_number.text

    return [part_number_text]

def one_url(url, desc='', outdir=OUTPUT_DIR, history_dir=HISTORY_DIR, work_name=WORK_NAME):
    print('<<<'+ url + '>>>')
    scraped_time_str = get_current_time_str()

    # 1. 이미 스크래핑한 목록에 있는지 검사
    column_names = ['scraped_time', 'output_file', 'url', 'desc']

    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    history_file = os.path.join(history_dir, f'{work_name}.txt')
    if not os.path.isfile(history_file) or os.path.getsize(history_file) == 0:
        with open(history_file, mode='w', encoding='utf-8') as f:
            f.write(HISTORY_FILE_SEP.join(column_names) + '\n')

    history_db = pd.read_csv(history_file, sep=HISTORY_FILE_SEP, names=column_names)
    if url in history_db['url'].values:
        print('Already in the history: ' + url)
        return

    # 2. 결과 저장 디렉토리 생성
    outdir = os.path.join(outdir, work_name)
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # 3. URL 경로의 마지막 값을 사용하여 결과 저장 파일 이름 정의
    # EX) https://www.mouser.kr/ProductDetail/Samsung-Electro-Mechanics/CL32Y476KPVVPNE?qs=HoCaDK9Nz5eDPpA1BTvjug%3D%3D
    parsed_url = urlparse(url)
    part_number = os.path.basename(parsed_url.path)

    filename = part_number if part_number is not None and len(part_number) > 0 else scraped_time_str
    output_file = os.path.join(outdir, f'{filename}.txt')

    # 4. URL 페이지 요청
    page = requests.get(url)
    if page.status_code != STATUS_CODE_SUCCESS:
        print(f'HTTP request failure: status_code = {page.status_code}')
        return
    
    if int(page.headers['Content-Length']) < CONTENT_LENGTH_MIN:
        print(f'Content-Length too short: length = {page.headers["Content-Length"]}')
        return

    # 5. 웹 페이지에서 텍스트 추출
    texts = extract_texts(page)

    # 6. 텍스트를 결과 파일에 저장
    with open(output_file, mode='w', encoding='utf-8') as f:
        #f.write(url + '\n')
        for text in texts:
            if text:
                f.write(text + '\n')

    # 7. 이력 파일에 추가
    new_history = HISTORY_FILE_SEP.join([scraped_time_str, output_file, url, desc])
    with open(history_file, mode='a', encoding='utf-8') as f:
        f.write(new_history + '\n')

    print('New history: ' + new_history)
    
def url_list(list_file, outdir=OUTPUT_DIR, history_dir=HISTORY_DIR, work_name=WORK_NAME):
    with open(list_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if len(line) == 0:
            continue
        pos = line.find(' ')
        url = line if pos < 0 else line[0:pos]
        desc = line[pos+1:] if pos > 0 else ''
        #print(f'{url} {desc}')
        one_url(url, desc, outdir, history_dir, work_name)
    
if __name__ == '__main__':
    try:
        fire.Fire({
            'one_url': one_url,
            'url_list': url_list
        })
    except:
        traceback.print_exc(file=sys.stdout)
