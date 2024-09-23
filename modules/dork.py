import json
from bs4 import BeautifulSoup
import time
import requests
import pickle
from urllib.parse import urlparse
import os

from .colors import RED, BLUE, WHITE, GREEN


def google_dork_all_pages(domain, output_dir, max_pages=10):
    print(f"\n====== (Sub)domains - Google Dorks ======")
    domain_file = os.path.join(output_dir, f"{domain}_domains.json")
    directory_file = os.path.join(output_dir, f"{domain}_directorys.json")
    cache_file = os.path.join("/tmp", f"{domain}_dorks.pkl")

    base_url = "https://www.google.com/search?q=site:{}&num=80&start={}"
    links = set()  # Using a set to only store unique values
    domains = set()

    def load_from_pickle():
        if os.path.exists(cache_file):
            with open(cache_file, "rb") as file:
                print(
                    f"Google results already exists for host: {domain}, {GREEN}loaded{WHITE} from {BLUE}{cache_file}{WHITE}"
                )
                return pickle.load(file)
        return None

    def save_to_pickle(results):
        with open(cache_file, "wb") as file:
            pickle.dump(results, file)
            print(
                f"Google results {GREEN}cached{WHITE} in file: {BLUE}{cache_file}{WHITE}"
            )

    cached_results = load_from_pickle()
    if cached_results:
        links, domains = cached_results
    else:
        for page in range(max_pages):
            start = page * 100
            url = base_url.format(domain, start)

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
                "Cache-Control": "max-age=0",
                "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "iframe",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-site",
                "upgrade-insecure-requests": "1",
                "referer": "https://www.google.com/",
            }

            try:
                print(f"Fetching results for page {page} from Google...")
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                html = response.text
                soup = BeautifulSoup(html, "html.parser")
                results = soup.find_all("div", class_="g")

                if not results:
                    break

                for result in results:
                    link = result.find("a", href=True)
                    if link:
                        links.add(link["href"])
                        unique_domains = urlparse(link["href"]).netloc
                        domains.add(unique_domains)
                time.sleep(3)

            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                break

        save_to_pickle((links, domains))

    for domain in list(domains):
        print(f"{BLUE}Found Domain{WHITE}: {domain}")

    with open(domain_file, "w") as file:
        json.dump(list(domains), file, indent=4)
        print(f"\n(sub)domains are {GREEN}saved{WHITE} in {BLUE}{domain_file}{WHITE}")

    with open(directory_file, "w") as file:
        json.dump(list(links), file, indent=4)
        print(
            f"The found directories are {GREEN}saved{WHITE} in {BLUE}{directory_file}{WHITE}"
        )
