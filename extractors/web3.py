from requests import get
from bs4 import BeautifulSoup


def extract_webThree_jobs(keyword):
    base_url = "https://web3.career/"
    response = get(f"{base_url}{keyword}-jobs")
    if response.status_code != 200:
        print("Can't request website")
        print(response.status_code)
    else:
        results = []
        soup = BeautifulSoup(response.text, "html.parser")
        jobs = soup.find("tbody", class_="tbody").find_all("tr", class_="table_row")
        for job in jobs:
            position_td, company_td, _, location_td, _, _ = job.find_all("td")
            position_anchor = position_td.find("a")
            link = position_anchor["href"]
            position = position_anchor.find("h2")
            company = company_td.find("h3")
            location_text = []
            for location in location_td:
                text = location.text
                location_text.append(text)
            location_list = map(str, location_text)
            location = "".join(location_list)
            if position == None:
                continue
            elif company == None:
                continue
            job_data = {
                "position": position.text,
                "company": company.text,
                "link": f"https://www.web3.carrer{link}",
                "location": location.strip(),
                "site": "web3",
            }
            results.append(job_data)
        print("web3 done")
        return results
