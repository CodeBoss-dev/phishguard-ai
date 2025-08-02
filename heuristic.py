import ipaddress
from urllib.parse import urlparse
import whois
from datetime import *

DOMAIN_AGE_THRESHOLD_DAYS = 100

def check_suspicious_url(url: str) -> int:
    score = 0
    lower_url = url.lower() # lower url to maintain integrity

    try:
        hostname = urlparse(url).hostname # Retrieve hostname from URL
        if hostname:
            try:
                ipaddress.ip_address(hostname) # Check if the URL contains IP Address If not, go to "ValueError"
                print("\nHost appears to be an IP Address")
                score += 5

            except ValueError:
                try:
                    domain_info = whois.whois(hostname) # Runs "whois" on hostname to retrieve details
                    creation_date = domain_info.creation_date

                    if creation_date:
                        if isinstance(creation_date, list): # Check if the "creation_date" is a list
                            creation_date = creation_date[0] # Pick the first element from the list

                        age_in_days = (datetime.now() - creation_date).days
                        print(f"Domain is {age_in_days} old")

                        if age_in_days < DOMAIN_AGE_THRESHOLD_DAYS:
                            print("Domain is suspiciously new")
                            score += 6
                    else:
                        print("Couldn't determine domain age")
                        score += 3
                except Exception as e:
                    print(f"Couldn't perform whois lookup for {hostname}")
                    score += 1

    except Exception as e:
        print(f"Hostname couldn't be found {e}")

    # Flag based on particular keywords in URL
    keyword = ["login", "update", "secure", "account", "verify", "signin", "password", "banking", "confirm", "webscr"]

    for keywords in keyword:
        if keywords in lower_url:
            print(f"Potential Risk Found {keywords}")
            score += 1

    return score

if __name__ == "__main__":
    test_url1 = "https://apple.com/"
    keyword_score1 = check_suspicious_url(test_url1)
    print(f"Final Keyword score {keyword_score1}")

    test_url2 = "http://192.168.1.1/secure/verify.php"
    keyword_score2 = check_suspicious_url(test_url2)
    print(f"Final Score {keyword_score2}")