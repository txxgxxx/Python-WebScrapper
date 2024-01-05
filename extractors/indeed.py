from requests import get
from bs4 import BeautifulSoup
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection


def get_page_count(keyword):
    base_url = "https://kr.indeed.com/jobs?q="
    SBR_WEBDRIVER = 'https://brd-customer-hl_e6fde474-zone-scraping_browser-country-kr:565yriq3kk05@brd.superproxy.io:9515'
    # print('Connecting to Scraping Browser...')
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        # print(f'Connected! Navigating to {base_url}{keyword}...')
        driver.get(f'{base_url}{keyword}')
        # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
        # print('Waiting captcha to solve...')
        solve_res = driver.execute('executeCdpCommand', {
            'cmd': 'Captcha.waitForSolve',
            'params': {'detectTimeout': 10000},
        })
        # print('Captcha solve status:', solve_res['value']['status'])
        # print('Navigated! Scraping page content...')
        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')
        pagination = soup.find("nav", attrs={"aria-label":"pagination"}).find('ul')
        pages = pagination.find_all('li', recursive=False)
        if not pages:
            return 1
        count = len(pages)
        for page in pages:
            a = page.find('a')
            # 지금 a는 파이썬 딕셔너리
            try:
                if a['aria-label'] == "Previous Page":
                    count-=1
                if a['aria-label'] == "Next Page":
                    count-=1
            except KeyError:
                count = count
            # aria_label = "aria_label"
            # if aria_label in a:
            #     if a['aria-label'] == "Previous Page":
            #         count-=1
            #     if a['aria-label'] == "Next Page":
            #         count-=1
            # Key Error 해결하기
        if count >= 5:
            return 5
        else:
            return count

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        final_url = f'{base_url}?q={keyword}&start={page*10}'
        SBR_WEBDRIVER = 'https://brd-customer-hl_e6fde474-zone-scraping_browser-country-kr:565yriq3kk05@brd.superproxy.io:9515'
        print('Connecting to Scraping Browser...')
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            print(f'Connected! Navigating to {final_url}...')
            driver.get(final_url)
            # CAPTCHA handling: If you're expecting a CAPTCHA on the target page, use the following code snippet to check the status of Scraping Browser's automatic CAPTCHA solver
            print('Waiting captcha to solve...')
            solve_res = driver.execute('executeCdpCommand', {
                'cmd': 'Captcha.waitForSolve',
                'params': {'detectTimeout': 10000},
            })
            print('Captcha solve status:', solve_res['value']['status'])
            print('Navigated! Scraping page content...')
            response = driver.page_source
            soup = BeautifulSoup(response, "html.parser")
            job_list = soup.find("ul", class_="css-zu9cdh eu4oa1w0")
            if job_list == None:
                print("error")
                return
            jobs = job_list.find_all('li', recursive=False)
            for job in jobs:
                zone = job.find("div", class_="mosaic-zone")
                if zone == None:
                    anchor = job.select_one("h2 a")
                    title = anchor['aria-label']
                    link = anchor['href']
                    company = job.find("span", attrs={"data-testid":"company-name"})
                    location = job.find("div", attrs={"data-testid":"text-location"})
                    job_data = {
                        'link': f"https://kr.indeed.com{link}",
                        'company': company.string.replace(",", " "),
                        'location': location.string.replace(",", " "),
                        'position' : title.replace(",", " ")
                    }
                    results.append(job_data)
    return results
