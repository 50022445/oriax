import dns.resolver
from .colors import RED, BLUE, WHITE

def get_ptr_record(ip):
    try:
        reverse_name = dns.reversename.from_address(ip)
        resolver = dns.resolver.Resolver()
        # Use Cloudflare DNS servers
        resolver.nameservers = ["1.1.1.1", "1.0.0.1"]

        ptr_records = resolver.resolve(reverse_name, "PTR")
        return [str(record) for record in ptr_records]
    except dns.resolver.NoAnswer or dns.resolver.NXDOMAIN:
        return "No PTR record found"
    except Exception as e:
        return f"Error: {e}"

def query_dns_info(domain):
    print(f"\n====== DNS Records ======")
    
    record_types = {
        "A": "A records",
        "AAAA": "AAAA records",
        "MX": "MX records",
        "NS": "NS records",
        "CNAME": "CNAME records",
    }

    for record_type, record_name in record_types.items():
        try:
            answers = dns.resolver.resolve(domain, record_type)
            print(f"{BLUE}{record_name}{WHITE}:")
            for rdata in answers:
                if record_type == "A":
                    ptr_record = get_ptr_record(rdata.to_text())
                    if "Error" in ptr_record:
                        ptr_record = "No PTR record found!"
                    print(f"\t{rdata.to_text()} ==> {ptr_record}")
                elif record_type == "MX":
                    print(
                        f"\tMailserver: {rdata.exchange}, Preference: {rdata.preference}"
                    )
                elif record_type == "NS":
                    print(f"\tNameserver: {rdata.target}")
                else:
                    print(f"\t{rdata.to_text()}")
        except dns.resolver.NoAnswer:
            print(f"\nNo {RED}{record_name}{WHITE} found!")
        except Exception as e:
            print(f"\n Error fetching {RED}{record_name}{WHITE}: {e}")