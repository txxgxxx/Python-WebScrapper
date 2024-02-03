import requests
from bs4 import BeautifulSoup


def get_page(keyword):
    baseUrl = "https://berlinstartupjobs.com/"
    response = requests.get(
        f"{baseUrl}skill-areas/{keyword}",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    soup = BeautifulSoup(response.content, "html.parser")
    page = soup.find("ul", class_="bsj-nav").find_all("a")
    if page is None or len(page) == 0:
        return 1
    else:
        pages = len(page)
        return pages


def extract_ber_jobs(keyword):
    jobs = []
    pages = get_page(keyword)
    for page in range(pages):
        page = page + 1
        print(f"extracting page {page}")
        baseUrl = "https://berlinstartupjobs.com/"
        response = requests.get(
            f"{baseUrl}skill-areas/{keyword}/page/{page}",
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            },
        )
        soup = BeautifulSoup(response.content, "html.parser")
        jobs = soup.find("ul", class_="jobs-list-items").find_all("li")
        for job in jobs:
            if type(job) == dict:
                continue
            header = job.find("div", class_="bjs-jlid__header")
            position = header.find("h4").text
            company = header.find("a", class_="bjs-jlid__b").text
            link = header.find("a", class_="bjs-jlid__b")["href"]
            description = job.find("div", class_="bjs-jlid__description").text
            job_data = {
                "position": position,
                "company": company,
                "link": link,
                "location": "-",
                "description": description.replace("\n", "")
                .replace("\t", "")
                .replace("\xa0", " "),
                "site": "ber",
            }
            jobs.append(job_data)
    print("ber done")
    return jobs
