import sys
from urllib.parse import urlparse
import os
import socket
from modules import dork, shodan, whois, dns, colors, headers

url = sys.argv[1]
domain = urlparse(url).netloc
ip = socket.gethostbyname(domain)

output_dir = os.path.dirname(f"output/{domain}/")
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir)


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


if __name__ == "__main__":
    banner()
    headers.check_sec_headers(url)
    dns.query_dns_info(domain)
    whois.get_whois_info(domain)
    shodan.query_shodan(ip, domain, output_dir)
    dork.google_dork_all_pages(domain, output_dir)
