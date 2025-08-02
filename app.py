# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

# --- Using your exact file and function names for imports ---
from scanner import scrape_website
from heuristic import check_suspicious_url
from brain import analyze_content_with_ai

# --- Flask App Setup ---
app = Flask(__name__)
# CORS is required to allow the browser extension to make requests to this server.
CORS(app)

# It is not safe to hardcode your API key.
# Load it from an environment variable for better security.
# To run this, you'll first type this in your terminal:
# export GEMINI_API_KEY='YOUR_AIza...'
my_api_key = os.environ.get("GEMINI_API_KEY")


def create_final_report(url: str) -> dict:
    """
    This function orchestrates the analysis using your modules and
    builds a complete report dictionary.
    """
    # --- Running Heuristic Analysis ---
    heuristic_score = check_suspicious_url(url)

    # --- Running Web Scraper ---
    scraped_text, scraping_error = scrape_website(url)

    # Initialize a default report for the AI part
    ai_report = {
        "ai_score": None,
        "justification": "AI analysis was skipped.",
        "verdict": "Unknown",
        "error": None
    }

    if scraping_error:
        print(f"Scraping Failed: {scraping_error}")
        ai_report["error"] = f"Scraping failed: {scraping_error}"
    elif scraped_text:
        # --- Starting AI Analysis ---
        # This calls the function from your brain.py
        ai_report = analyze_content_with_ai(scraped_text, api_key=my_api_key)
    else:
        ai_report["error"] = "Scraping returned no text."

    # --- Aggregating the Final Report ---
    # Combine the heuristic score and the AI report into one object
    final_report = {
        "url": url,
        "heuristic_score": heuristic_score,
        "ai_score": ai_report.get("ai_score"),
        "ai_justification": ai_report.get("justification"),
        "final_verdict": ai_report.get("verdict"),
        "analysis_errors": ai_report.get("error")
    }
    return final_report


@app.route('/analyze', methods=['POST'])
def analyze_endpoint():
    """
    This is the API endpoint that the browser extension will call.
    """
    if not my_api_key:
        return jsonify({"error": "API key is not configured on the server."}), 500

    # Get the URL from the incoming JSON request
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided in the request."}), 400

    url_to_analyze = data['url']

    try:
        # Run the full analysis and get the final report
        report = create_final_report(url_to_analyze)
        # Send the report back to the extension as JSON
        return jsonify(report)
    except Exception as e:
        # Catch any unexpected errors during analysis
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # This makes the server run
    print("Starting PhishGuard AI server...")
    print("To use, run this in your terminal: export GEMINI_API_KEY='YOUR_KEY_HERE'")
    app.run(debug=True, port=5000)

