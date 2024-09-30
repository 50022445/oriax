# Oriax
> A fast and simple tool for information-gathering.

Oriax is a Python-based information-gathering tool used to find various types of information about a domain.

**The project is under heavy development, so please be aware!**

## How does it work? 🤠
Oriax uses a collection of public services to enumerate all sorts of useful information on your target.
These services are:
* DNS records
* WHOIS Database
* Shodan API
* Google Dorks

Some of these services can be quite annoying when queried too much (E.g. Google). That's why Oriax makes use of a cache system, these cached results can be found in your **/tmp** directory :innocent:

Note: To use the Shodan API, make sure you have a valid Shodan API key.

## Installation :wrench:

This tool uses [Poetry](https://python-poetry.org/docs/) for dependency-management.
Please make sure you have Poetry installed :wink:

#### OSX & Linux:

```sh
git clone https://github.com/50022445/oriax.git
cd oriax && poetry install
```

## Usage
```sh
usage: main.py [-h] [--all] [--headers] [--dns] [--whois] [--shodan] [--dork] url

positional arguments:
  url         Target URL

options:
  -h, --help  show this help message and exit
  --all       Run all functions
  --headers   Check security headers
  --dns       Query DNS information
  --whois     Get WHOIS information
  --shodan    Query Shodan data (Needs valid API token)
  --dork      Run Google Dork
```

#### Examples
```sh
# Use all functions
python3 main.py --all https://example.com
```
```sh
# Query the WHOIS data and DNS records
python3 main.py --whois --dns https://example.com #
```
```sh
# Only query the Shodan API
python3 main.py --shodan https://example.com
```

## Roadmap
- [x] Implement Google Dork function for (sub)domain enumeration.
- [x] Implement caching in query functions to make the program alot faster.
- [x] Move each function to its own 'module' to make the code easier to read.
- [x] Add argument support.
- [ ] Add proxy support.
- [ ] Code refactor.

