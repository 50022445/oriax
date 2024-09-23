import requests
from .colors import RED, GREEN, WHITE

def check_sec_headers(url):
    print(f"====== Security Headers ======")
    try:
        response = requests.head(url)
        security_headers = {
            "X-Content-Type-Options": response.headers.get("x-content-type-options"),
            "X-XSS-Protection": response.headers.get("x-xss-protection"),
            "Strict-Transport-Security": response.headers.get(
                "strict-transport-security"
            ),
            "Content-Security-Policy": response.headers.get("content-security-policy"),
            "Referrer-Policy": response.headers.get("referrer-policy"),
            "X-Frame-Options": response.headers.get("x-frame-options"),
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