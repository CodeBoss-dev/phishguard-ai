from scanner import scrape_website
from heuristic import check_suspicious_url
from brain import analyze_content_with_ai

def analyze(url: str, api_key: str):
    print(f"\n{'='*20}\nStarting Analysis for {url}\n{'='*20}")

    print("\n---Running Heuristic Analysis---")
    heuristic_score = check_suspicious_url(url)
    print(f"Heuristic Score = {heuristic_score}")

    print("\n---Running Web Scraper---")
    scraped_text, error = scrape_website(url)
    if error:
        print(f"Scraping Failed: {error}")
        exit(0)
    else:
        print(f"\n{'='*20}\nStarting AI Analysis for {url}\n{'='*20}")
        report = analyze_content_with_ai(scraped_text, api_key=api_key)

        return report

if __name__ == "__main__":
    my_api_key = "YOUR_API_KEY_HERE"
    test_url = "https://apextradetune.click/"
    report = analyze(test_url, my_api_key)

    print(report)

