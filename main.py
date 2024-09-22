import requests
import sys
from colorama import Fore, init
import dns.resolver
from urllib.parse import urlparse
import whois
import shodan
from dotenv import load_dotenv
import os
import socket
from pprint import pprint
import yaml

init()
GREEN = Fore.GREEN
RED = Fore.RED
WHITE = Fore.WHITE
BLUE = Fore.BLUE
MAGENTA = Fore.MAGENTA

load_dotenv()
api = shodan.Shodan(os.getenv('SHODAN_API_KEY'))

url = sys.argv[1]
domain = urlparse(url).netloc
ip = socket.gethostbyname(domain)

def banner():
    print(f""" {BLUE}
▄██████▄     ▄████████  ▄█     ▄████████ ▀████    ▐████▀ 
███    ███   ███    ███ ███    ███    ███   ███▌   ████▀  
███    ███   ███    ███ ███▌   ███    ███    ███  ▐███    
███    ███  ▄███▄▄▄▄██▀ ███▌   ███    ███    ▀███▄███▀    
███    ███ ▀▀███▀▀▀▀▀   ███▌ ▀███████████    ████▀██▄     
███    ███ ▀███████████ ███    ███    ███   ▐███  ▀███    
███    ███   ███    ███ ███    ███    ███  ▄███     ███▄  
▀██████▀    ███    ███ █▀     ███    █▀  ████       ███▄ 
            ███    ███                                   
                                    {WHITE}Made with {MAGENTA}<3{WHITE}
    """)

def check_sec_headers(url):
    print(f"====== Security Headers ======")
    try:
        response = requests.head(url)
        security_headers = {
            "X-Content-Type-Options": response.headers.get("x-content-type-options"),
            "X-XSS-Protection": response.headers.get("x-xss-protection"),
            "Strict-Transport-Security": response.headers.get("strict-transport-security"),
            "Content-Security-Policy": response.headers.get("content-security-policy"),
            "Referrer-Policy": response.headers.get("referrer-policy"),
            "X-Frame-Options": response.headers.get("x-frame-options")
        }

        if security_headers is not None:
            for key, value in security_headers.items():
                if value is not None:
                    print(f"{GREEN}{key}{WHITE}: {value}")

            for key, value in security_headers.items():
                if value is None:
                    print(f"{RED}{key}{WHITE}: Not Found!")
    except Exception as e:
        print(f"An {RED}error{WHITE} occured: {e}")


def query_dns_info(domain):
    print(f"\n====== DNS Records ======")

    record_types = {
        'A': 'A records',
        'AAAA': 'AAAA records',
        'MX': 'MX records',
        'NS': 'NS records',
        'CNAME': 'CNAME records'
    }

    for record_type, record_name in record_types.items():
        try:
            answers = dns.resolver.resolve(domain, record_type)
            print(f"{BLUE}{record_name}{WHITE}:")
            for rdata in answers:
                if record_type == 'MX':
                    print(f"\tMailserver: {rdata.exchange}, Preference: {rdata.preference}")
                elif record_type == 'NS':
                    print(f"\tNameserver: {rdata.target}")
                else:
                    print(f"\t{rdata.to_text()}")
        except dns.resolver.NoAnswer:
            print(f"\nNo {RED}{record_name}{WHITE} found!")
        except Exception as e:
            print(f"\n Error fetching {RED}{record_name}{WHITE}: {e}")

def get_whois_info(domain):
    print(f"\n====== WHOIS Info ======")
    try:
        domain_info = whois.whois(domain)

        record_types = {
            'Domain': 'domain',
            'Registrar': 'registrar',
            'Creation Date': 'creation_date',
            'Expiration Date': 'expiration_date',
            'WHOIS Server': 'whois_server',
            'ORG': 'org',
            'Address': 'address',
            'City': 'city',
            'Postal Code': 'registrant_postal_code',
            'Country': 'country',
            'Emails': 'emails',
            'Name': 'name',
        }

        for record_type, record_name in record_types.items():
            try:
                print(f"{BLUE}{record_type}{WHITE}: {getattr(domain_info, record_name)}")
            except Exception as e:
                print(f"An {RED}error{WHITE} occured: {e}")
    except whois.parser.PywhoisError as e:
        print(f"An {RED}error{WHITE} occured: {e}")

def query_shodan(ip):
    print(f"\n====== Shodan Info ======")
    shodan_output = f"{domain}_shodan.yaml"

    records_types = {
        'ASN': 'asn',
        'City': 'city',
        'Country Code': 'country_code',
        'Country Name': 'country_name',
        'Ports': 'ports',
        'ORG': 'org',
        'ISP': 'isp',
        'IP': 'ip_str',
        'Domains': 'domains'
    }

    try:
        if os.path.exists(shodan_output):
            print(f"Shodan results already exists for host: {domain}, {GREEN}saved{WHITE} in {BLUE}{shodan_output}{WHITE}")
            with open(shodan_output, 'r') as file:
                host_info = yaml.safe_load(file)
                for record_type, record_name in records_types.items():
                    print(f"{BLUE}{record_type}{WHITE}: {host_info.get(record_name)}")
        else:
            host_info = api.host(ip)
            with open(shodan_output, 'w') as file:
                yaml.dump(host_info, file, default_flow_style=False)

            for record_type, record_name in records_types.items():
                print(f"{BLUE}{record_type}{WHITE}: {host_info.get(record_name)}")

            print(f"\nShodan results {GREEN}saved{WHITE} in {BLUE}{shodan_output}{WHITE}")

    except shodan.APIError as e:
        print(f"An {RED}error{WHITE} occured: {e}")

if __name__ == "__main__":
    banner()
    check_sec_headers(url)
    query_dns_info(domain)
    get_whois_info(domain)
    query_shodan(ip)
