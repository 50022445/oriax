import whois
import pickle
import os

from .colors import RED, BLUE, WHITE, GREEN


def get_whois_info(domain):
    print(f"\n====== WHOIS Info ======")
    cache_file = os.path.join("/tmp", f"{domain}_whois.pkl")

    record_types = {
        "Domain": "domain",
        "Registrar": "registrar",
        "Creation Date": "creation_date",
        "Expiration Date": "expiration_date",
        "WHOIS Server": "whois_server",
        "ORG": "org",
        "Address": "address",
        "City": "city",
        "Postal Code": "registrant_postal_code",
        "Country": "country",
        "Emails": "emails",
        "Name": "name",
    }

    if os.path.exists(cache_file):
        print(f"Using {GREEN}cached{WHITE} WHOIS information for host: {domain}")
        with open(cache_file, "rb") as file:
            domain_info = pickle.load(file)
    else:
        try:
            domain_info = whois.whois(domain)
            with open(cache_file, "wb") as file:
                pickle.dump(domain_info, file)
                print(f"WHOIS results cached in file: {BLUE}{cache_file}{WHITE}")
        except whois.parser.PywhoisError as e:
            print(f"An {RED}error{WHITE} occured: {e}")

    for record_type, record_name in record_types.items():
        try:
            print(f"{BLUE}{record_type}{WHITE}: {getattr(domain_info, record_name)}")
        except Exception as e:
            print(f"An {RED}error{WHITE} occured: {e}")
