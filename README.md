# WHOIS Domain Intelligence Tool 🕵️‍♂️

A Python-based Open-Source Intelligence (OSINT) utility built for SOC analysts to rapidly footprint suspect domain infrastructure during phishing investigations and incident response.

**Features:**
* Utilizes the `python-whois` library to programmatically query global WHOIS registries.
* Parses and formats chaotic raw WHOIS data into clean, structured intelligence (Registrar, Creation/Expiration dates, Name Servers).
* Employs Python `threading` to prevent GUI lockups while awaiting external server responses.
* Gracefully handles domain privacy protections (GDPR redactions) and missing data fields.

*Built as Day 14 of a 30-Day Network Engineering & Security portfolio streak.*
