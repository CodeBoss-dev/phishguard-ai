from bs4 import BeautifulSoup
import requests

def scrape_website(url) -> tuple[str | None, str | None]:
    try:
        # Headers required to imitate as an actual browser 
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=10)

        response.raise_for_status()  # Raise an error for bad responses
        print("Website fetching successful.")

        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract "script" and "style" tag from soup data
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()  # Remove these elements
        text = soup.get_text(separator=' ', strip=True) # separator to add a space ' ' between semantic tag's text, strip to remove whitespaces, leading and trailing

        return text, None
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None, http_err
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, e

if __name__ == "__main__":
    test_url = "https://www.apple.com"
    extracted_text, error = scrape_website(test_url) # Tuple (str | None, str | None)
    if error:
        print(f"Error occurred: {error}")
    else:
        print(f"Extracted text length: {len(extracted_text)} characters")
        print(f"First 500 characters of extracted text: {extracted_text[:500]}")
    print("Scraping completed.")
