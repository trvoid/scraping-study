################################################################################
# Selenium Test
################################################################################

import os, sys, traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService # Chrome 예시
from selenium.webdriver.chrome.options import Options as ChromeOptions
# from selenium.webdriver.edge.service import Service as EdgeService # Edge 예시
# from selenium.webdriver.firefox.service import Service as FirefoxService # Firefox 예시
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

################################################################################
# Functions
################################################################################

def extract_texts(content):
    soup = BeautifulSoup(content, 'html.parser')

    # 부품 번호
    part_number = soup.find(id='spnManufacturerPartNumber')
    if part_number:
        part_number_text = part_number

    return [part_number_text]

def create_driver():
    # 원하는 User-Agent 문자열
    user_agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"    
    # 다른 User-Agent 예시: "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
    referer = "https://www.mouser.kr/c/passive-components/capacitors/ceramic-capacitors/?m=Samsung%20Electro-Mechanics&termination%20style=SMD%2FSMT&voltage%20rating%20dc=10%20VDC"
    cookie = 'akacd_Default_PR=3924655309~rv=98~id=3b13a33162c647a207b5850b3779bf17; ASP.NET_SessionId=utptxkdlhc1alde3mww3f1ad; CARTCOOKIEUUID=16ba8842-6d5d-47e9-a968-844f0544e637; PIM-SESSION-ID=UbTHRl9S6X6Ct7NQ; __neoui=abd7a1d8-2d36-4480-9a0b-cd4580a3b651; _fbp=fb.1.1747202525571.10668820579293219; LPVID=hkNzU4NDAxYzliZjRkZGNj; __RequestVerificationToken=vi1zvs4-wnDfAIThvCgikjmyTcQviep4pCtXT90yF58f9k_AEfJ62--swvCe-_YXrBcw_FDkX6qVxb43fpeoK2uBJGk1; AKA_A2=A; ak_bmsc=8352FB5DDB470A6027535A67B777DC9F~000000000000000000000000000000~YAAQFtojF5dX/uqWAQAAg/MJ8htJ4kErHAIJukTE9aE7dMwBxMJpcB6flnP6k5W50iUx6oTAqPmfyIIocL5cVjZLOBwM1waubpQ49XpHv9AFLj3jNnTOnVm8gCg0hnZIsdTPMTL7NcwNfZbPVcg4Zj+d+LpfYPxlBpdYSko0/Fl3h3f45XY5Vxng/w24giru7sXO+0iAwpNFTznj22gkWSiPWDGqDiTi0qooWiBGN0XH8mJG61jKyfzXJtow1x47a8NFdgoQvQ6T0K6UV7KnorKoS/p0hTt5L+i44E8VLfLazQRdI2zPQmstCzp8Mw7WBuWX/OlQRCOWDd/EHqsUDPia+REoBjwViq7lfxkm0iIsGPdhwZQEwopgdtzYQlg0UenJQlmLDP2oPYSHfOGDP2qIiYhAl7KnFJ/YP73JNIcDrGFRPBRToSw4da3eJyrLSQw=; _ga_15W4STQT4T=deleted; _gid=GA1.2.1617356575.1747817465; bm_ss=ab8e18ef4e; _fs_dwell_passed=7997736d-d053-4443-8ce2-1fed4348cb4a; _gcl_au=1.1.2065923324.1747202524.852675389.1747817525.1747817550; preferences=pl=ko-KR&pc_kr=KRW; LPSID-12757882=YwWLYF6uRUimxkXiv36fuQ; QSI_HistorySession=https%3A%2F%2Fwww.mouser.kr%2F~1747202537130%7Chttps%3A%2F%2Fwww.mouser.kr%2Fc%2Fpassive-components%2Fcapacitors%2Fmlccs%2F~1747202583468%7Chttps%3A%2F%2Fwww.mouser.kr%2FProductDetail%2FSamsung-Electro-Mechanics%2FCL05CR75CB5NNWC%3Fqs%3D81r%25252BiQLm7BRa8DJl4bW9KQ%253D%253D~1747202645824%7Chttps%3A%2F%2Fwww.mouser.kr%2FProductDetail%2FSamsung-Electro-Mechanics%2FCL32Y476KPVVPNE%3Fqs%3DHoCaDK9Nz5eDPpA1BTvjug%253D%253D~1747817611810; bm_so=D88166D8B31B4E5CE3ADB3104122294E8E80D5EECD90F3EAC7385556EF2FB919~YAAQleQ1F5YJXNSWAQAAH6Yz8gOYCcGpQd5RyANrmEXbnlEGufd9nOKKEI55YHM2GZjyIAah6PGXHXsK80TcyCAeXJ8MNVgtCmfiV5ITVfesHKIHEUTdy0roGrW7m304fmJPtqjoYjMZwTu0IGloNOdiTO/bqjvPmrtBipIGFmHPRTm5lnHAO+HNv9bM0zFIr/NWDY/HR5sn6MSh/n9947w964cGsCZq3lk4/pVWaFUrCe+kAizZbAg1A/mjO38Txge1IqjvRlrt22AIVq5za9taI7s1e/Ui+w+6Gw4DbDRAhrsQYvdheN9mc89ZmCyqzMnXn8uopNH8unzqprILm+ph5HcfvBdNPTsqQCNi4lklp809fwc9jjkiHzH2pCQYdyUlF8GIi+x5cTmR42EUIAjcHmmyZjTa8DNyeASVHEHnQp69/x1DogeT0rHN6173cmu+pXZ1qgIUe6MMKOI=; bm_s=YAAQleQ1F5ELXNSWAQAA+LEz8gNQgMN3GcTQEaLAsLEgIuarxu0ePzw00XyOd2qb+PvgWzbhDzeYjkPwLp2y+4jpZP3Iowriv2Z295bW5rPgSVoDJFAyZX/Amn8kQCfWTEHYaAEgaJBhTP10zTLuUMRWhzqMyUvV3c03ZzQoc+V8a5NJGjjvUUcSQOBUkw0KghVxOfDRrtHeQmcf5CoWhwe7ZdU/jGj0g7Hkjv+iwhQ9+JYsCWZx19EgA1AB6HEqDRc3zfXzcUSoND0GKGOH4DTqFat1uhGnAIsWee9Z8I7Dwu+lhKOJfaNI77k3r30MCvZjUJkd2SkU5U5otdSmHIRSffvOY0CevIqmqc8xPtvy9ew33LhP7DDwyCmGkbu4PhITgf1jdv4djFT8r/Hkv0OjyZeT3lUNWq1Wxwoo+hTuj88LFfdPdujwQ0HcxWRtWiw/0roiUfAa9fw95iwv1JWfdxaxnll6wz5l7j0EsylUiOlp1cU1me9xVO9KmVCh3o7b5QoqGZwSox4yF1Wju4cBSI4mwlN9IQRCgv4yYGh78tOJe02vGra0rKzQgDw7bDXiJGpV; OptanonAlertBoxClosed=2025-05-21T09:36:37.309Z; OptanonConsent=isGpcEnabled=0&datestamp=Wed+May+21+2025+18%3A36%3A38+GMT%2B0900+(%ED%95%9C%EA%B5%AD+%ED%91%9C%EC%A4%80%EC%8B%9C)&version=202501.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=7c820f20-e63e-4cef-b0dd-3922386a059b&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0004%3A1%2CC0003%3A1%2CC0002%3A1%2CC0001%3A1&AwaitingReconsent=false&geolocation=KR%3B41; _rdt_uuid=1747202524973.e6271420-c2f8-403b-a25d-97a475b6488b; _ga=GA1.2.2099317169.1747202525; fs_uid=#Z1BBJ#33a34f5a-1aff-4721-b941-8fe86474ac8e:7997736d-d053-4443-8ce2-1fed4348cb4a:1747817464866::6#/1778738544; bm_lso=D88166D8B31B4E5CE3ADB3104122294E8E80D5EECD90F3EAC7385556EF2FB919~YAAQleQ1F5YJXNSWAQAAH6Yz8gOYCcGpQd5RyANrmEXbnlEGufd9nOKKEI55YHM2GZjyIAah6PGXHXsK80TcyCAeXJ8MNVgtCmfiV5ITVfesHKIHEUTdy0roGrW7m304fmJPtqjoYjMZwTu0IGloNOdiTO/bqjvPmrtBipIGFmHPRTm5lnHAO+HNv9bM0zFIr/NWDY/HR5sn6MSh/n9947w964cGsCZq3lk4/pVWaFUrCe+kAizZbAg1A/mjO38Txge1IqjvRlrt22AIVq5za9taI7s1e/Ui+w+6Gw4DbDRAhrsQYvdheN9mc89ZmCyqzMnXn8uopNH8unzqprILm+ph5HcfvBdNPTsqQCNi4lklp809fwc9jjkiHzH2pCQYdyUlF8GIi+x5cTmR42EUIAjcHmmyZjTa8DNyeASVHEHnQp69/x1DogeT0rHN6173cmu+pXZ1qgIUe6MMKOI=^1747820211149; datadome=Zj6I6F6GiLllEwhgAoEVKF8e_6RQk22PfiVzMMyURQ4YHeE~O5Pf54gb2R50~e82hN23BZBPRkjxgfyiHppMXZU97DXE~O4i0S97W_IbByIT0wU~ctfAkA5~tYE6o0g3; fs_lua=1.1747820762368; RT="z=1&dm=mouser.kr&si=d3f695d9-26b3-401f-88d4-aa7b80c7a4ec&ss=maxr0kar&sl=0&tt=0&bcn=%2F%2F684d0d45.akstat.io%2F&hd=e035"; _ga_15W4STQT4T=GS2.1.s1747820199$o2$g1$t1747820846$j58$l0$h0$doNbJe8RQPyZfiWu-yecQDNGUqsA0KtJT2A'

    # Chrome 옵션 설정
    chrome_options = ChromeOptions()
    chrome_options.add_argument(f'Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
    chrome_options.add_argument(f'Accept-Encoding=gzip, deflate, br, zstd')
    chrome_options.add_argument(f'Accept-Language=ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7')
    chrome_options.add_argument(f'Cache-Control=max-age=0')
    chrome_options.add_argument(f'Referer={referer}')
    chrome_options.add_argument(f'Cookie={cookie}')
    chrome_options.add_argument(f'Connection=keep-alive')
    chrome_options.add_argument(f'Host=www.mouser.kr')
    chrome_options.add_argument(f'Sec-Ch-Ua-Device-Memory=8')
    chrome_options.add_argument(f'Sec-Ch-Ua="Chromium";v="136", "Google Chrome";v="136", "Not.A/Brand";v="99"')
    chrome_options.add_argument(f'Sec-Ch-Ua-Arch="x86"')
    chrome_options.add_argument(f'Sec-Ch-Ua-Full-Version-List="Chromium";v="136.0.7103.114", "Google Chrome";v="136.0.7103.114", "Not.A/Brand";v="99.0.0.0"')
    chrome_options.add_argument(f"Sec-Ch-Ua-Mobile=?0")
    chrome_options.add_argument(f'Sec-Ch-Ua-Model=""')
    chrome_options.add_argument(f'Sec-Ch-Ua-Platform="Windows"')
    chrome_options.add_argument(f'Sec-Fetch-Dest=document')
    chrome_options.add_argument(f'Sec-Fetch-Mode=navigate')
    chrome_options.add_argument(f'Sec-Fetch-Site=same-origin')
    chrome_options.add_argument(f'Upgrade-Insecure-Requests=1')
    chrome_options.add_argument(f'Sec-Fetch-User=?1')
    chrome_options.add_argument(f'User-Agent={user_agent_string}')
    # chrome_options.add_argument("--headless") # 필요시 헤드리스 모드

    # --- 웹 드라이버 경로 설정 (PATH에 추가하지 않은 경우) ---
    # Chrome 예시 (chromedriver.exe 파일이 있는 전체 경로)
    #CHROME_DRIVER_PATH = "C:/WebDriver/chromedriver.exe" # 실제 경로로 수정하세요.
    # Edge 예시
    # EDGE_DRIVER_PATH = "C:/WebDriver/msedgedriver.exe"
    # Firefox 예시
    # FIREFOX_DRIVER_PATH = "C:/WebDriver/geckodriver.exe"

    # --- WebDriver 서비스 설정 (Selenium 4 이상 권장 방식) ---
    # Chrome 예시
    #service = ChromeService(executable_path=CHROME_DRIVER_PATH)
    #driver = webdriver.Chrome(service=service)

    # Edge 예시
    # service = EdgeService(executable_path=EDGE_DRIVER_PATH)
    # driver = webdriver.Edge(service=service)

    # Firefox 예시
    # service = FirefoxService(executable_path=FIREFOX_DRIVER_PATH)
    # driver = webdriver.Firefox(service=service)

    # --- WebDriver가 PATH에 설정되어 있다면 ---
    # service 객체 생성 시 executable_path를 명시하지 않아도 됩니다.
    # 예: driver = webdriver.Chrome() 또는 driver = webdriver.Edge()
    driver = webdriver.Chrome(options=chrome_options)

    return driver

################################################################################
# Main
################################################################################

def main(url):
    try:
        driver = create_driver()

        # 특정 웹사이트 열기
        driver.get(url)

        # 페이지 제목 출력
        print(f"페이지 제목: {driver.title}")

        # 5초 동안 대기
        # 방법 1: 간단한 시간 지연 (항상 좋은 방법은 아님)
        # time.sleep(5)

        # 방법 2: WebDriverWait 사용 (더 안정적)
        # 예: 특정 요소가 나타날 때까지 최대 10초 대기
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.specs-table"))
            )
            print("동적 콘텐츠 로딩 확인됨 (table.specs-table).")
        except Exception as e:
            print(f"지정한 요소 로딩 대기 중 타임아웃 또는 오류: {e}")
            # 콘텐츠가 없어도 계속 진행하거나, 여기서 종료할 수 있습니다.

        # 간단한 요소 찾기 예시 (페이지에 따라 다름)
        # h1_element = driver.find_element(By.TAG_NAME, "h1")
        # print(f"H1 태그 내용: {h1_element.text}")

        texts = extract_texts(driver.page_source)
        for text in texts:
            print(text)
    finally:
        # 브라우저 닫기
        driver.quit()

mouser_url = "https://www.mouser.kr/ProductDetail/Samsung-Electro-Mechanics/CL32Y476KPVVPNE?qs=HoCaDK9Nz5eDPpA1BTvjug%3D%3D"

if __name__ == "__main__":
    try:
        main(mouser_url)
    except:
        traceback.print_exc(file=sys.stdout)
