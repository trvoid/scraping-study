################################################################################
# 원불교신문 스크래핑
################################################################################

import os, sys, traceback
from datetime import datetime
import fire
import pandas as pd
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup

def get_current_time_str():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

def extract_texts(page):
    soup = BeautifulSoup(page.content, 'html.parser')
    
    head_content = soup.find('h3', class_='heading')
    if head_content:
        head_text = head_content.text

    info_content = soup.find('ul', class_='infomation')
    if info_content:
        info_items = info_content.find_all('li')
        if len(info_items) >= 2:
            date_text = info_items[1].text

    article_content = soup.find(id='article-view-content-div')
    if article_content:
        article_text = article_content.text

    return [head_text, date_text, article_text]

def main(url, outdir='output', history_file='history.txt'):
    scraped_time_str = get_current_time_str()

    # 1. 이미 스크래핑한 목록에 있는지 검사
    if not os.path.isfile(history_file):
        with open(history_file, mode='w', encoding='utf-8') as f:
            f.write('scraped_time,output_file,url\n')

    history_db = pd.read_csv(history_file)
    url_cols = history_db.iloc[:, 2]
    if url in url_cols.values:
        print('Found in the history: ' + url)
        return

    # 2. 결과 저장 디렉토리 생성
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    # 3. URL 파라미터 'idxno' 값을 사용하여 결과 저장 파일 이름 정의
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    idxno = query_params.get('idxno', None)

    filename = idxno[0] if idxno and len(idxno) > 0 else scraped_time_str
    output_file = os.path.join(outdir, f'{filename}.txt')

    # 4. URL 페이지 요청
    page = requests.get(url)

    # 5. 웹 페이지에서 텍스트 추출
    texts = extract_texts(page)

    # 6. 텍스트를 결과 파일에 저장
    with open(output_file, mode='w', encoding='utf-8') as f:
        #f.write(url + '\n')
        for text in texts:
            if text:
                f.write(text + '\n')

    # 7. 이력 파일에 추가
    history = f'{scraped_time_str},{output_file},{url}'
    with open(history_file, mode='a', encoding='utf-8') as f:
        f.write(history + '\n')

    print('Added a history: ' + history)
    
if __name__ == '__main__':
    try:
        fire.Fire(main)
    except:
        traceback.print_exc(sys.stdout)
