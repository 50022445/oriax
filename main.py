import sys
from urllib.parse import urlparse
import os
import socket
import argparse
from modules import dork, shodan, whois, dns, colors, headers

# Define the banner function
def banner():
    print(
        f""" {colors.BLUE}
▄██████▄     ▄████████  ▄█     ▄████████ ▀████    ▐████▀ 
███    ███   ███    ███ ███    ███    ███   ███▌   ████▀  
███    ███   ███    ███ ███▌   ███    ███    ███  ▐███    
███    ███  ▄███▄▄▄▄██▀ ███▌   ███    ███    ▀███▄███▀    
███    ███ ▀▀███▀▀▀▀▀   ███▌ ▀███████████    ████▀██▄     
███    ███ ▀███████████ ███    ███    ███   ▐███  ▀███    
███    ███   ███    ███ ███    ███    ███  ▄███     ███▄  
▀██████▀    ███    ███ █▀     ███    █▀  ████       ███▄ 
            ███    ███                                   
                                    {colors.WHITE}Made with {colors.MAGENTA}<3{colors.WHITE}
    """
    )

# Function to get domain and IP
def get_domain_and_ip(url):
    domain = urlparse(url).netloc
    ip = socket.gethostbyname(domain)
    return domain, ip

# Function to ensure output directory exists
def ensure_output_dir(domain):
    output_dir = os.path.dirname(f"output/{domain}/")
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# Main function to handle arguments and execute functions
def main():
    banner()
    parser = argparse.ArgumentParser(description='Web reconnaissance tool')
    parser.add_argument('url', help='Target URL')
    parser.add_argument('--all', action='store_true', help='Run all functions')
    parser.add_argument('--headers', action='store_true', help='Check security headers')
    parser.add_argument('--dns', action='store_true', help='Query DNS information')
    parser.add_argument('--whois', action='store_true', help='Get WHOIS information')
    parser.add_argument('--shodan', action='store_true', help='Query Shodan data')
    parser.add_argument('--dork', action='store_true', help='Run Google Dork')

    args = parser.parse_args()

    url = args.url
    domain, ip = get_domain_and_ip(url)
    output_dir = ensure_output_dir(domain)

    # Execute based on arguments
    if args.all or args.headers:
        headers.check_sec_headers(url)
    if args.all or args.dns:
        dns.query_dns_info(domain)
    if args.all or args.whois:
        whois.get_whois_info(domain)
    if args.all or args.shodan:
        shodan.query_shodan(ip, domain, output_dir)
    if args.all or args.dork:
        dork.google_dork_all_pages(domain, output_dir)

if __name__ == "__main__":
    main()
