import whois
import shodan
from dotenv import load_dotenv
import os
import yaml
import pickle

from .colors import RED, BLUE, WHITE, GREEN

load_dotenv()
api = shodan.Shodan(os.getenv("SHODAN_API_KEY"))


def query_shodan(ip, domain, output_dir):
    print(f"\n====== Shodan Info ======")
    output_file = f"{domain}_shodan.yaml"
    shodan_output = os.path.join(output_dir, output_file)

    records_types = {
        "ASN": "asn",
        "City": "city",
        "Country Code": "country_code",
        "Country Name": "country_name",
        "Ports": "ports",
        "ORG": "org",
        "ISP": "isp",
        "IP": "ip_str",
        "Domains": "domains",
    }

    try:
        if os.path.exists(shodan_output):
            print(
                f"Shodan results already exists for host: {domain}, {GREEN}saved{WHITE} in {BLUE}{shodan_output}{WHITE}"
            )
            with open(shodan_output, "r") as file:
                host_info = yaml.safe_load(file)
                for record_type, record_name in records_types.items():
                    print(f"{BLUE}{record_type}{WHITE}: {host_info.get(record_name)}")
        else:
            host_info = api.host(ip)
            with open(shodan_output, "w") as file:
                yaml.dump(host_info, file, default_flow_style=False)

            for record_type, record_name in records_types.items():
                print(f"{BLUE}{record_type}{WHITE}: {host_info.get(record_name)}")

            print(
                f"\nShodan results {GREEN}saved{WHITE} in {BLUE}{shodan_output}{WHITE}"
            )

    except shodan.APIError as e:
        print(f"An {RED}error{WHITE} occured: {e}")
