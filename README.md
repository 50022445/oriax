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

Note: To use the Shodan API, make sure you have a valid Shodan API key.

## Installation

This tool uses [Poetry](https://python-poetry.org/docs/) for dependency-management.
Please make sure you have Poetry installed :wink:

#### OSX & Linux:

```sh
git clone https://github.com/50022445/oriax.git \
cd oriax && poetry init
```

## Usage

```sh
python3 oriax.py https://example.com
```

## Roadmap
- [x] Implement Google Dork function for (sub)domain enumeration.
- [x] Implement caching in query functions to make the program alot faster.
- [x] Move each function to its own 'module' to make the code easier to read.
- [ ] Add argument support.
- [ ] Add proxy support?

