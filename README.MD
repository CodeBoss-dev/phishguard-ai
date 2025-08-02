# PhishGuard AI 🛡️

**A Multi-Vector Phishing Analysis Engine using Heuristics and Generative AI.**

PhishGuard AI is an intelligent tool that analyzes a given URL for phishing threats. It combines traditional, rule-based heuristic checks with advanced, AI-driven analysis of webpage content to generate a real-time, comprehensive risk score.

## Core Thesis

Traditional phishing detection relies on blacklists or simple URL analysis, which sophisticated attackers can easily bypass. This project posits that a more robust defense is achieved by augmenting these heuristics with a Large Language Model (LLM). The LLM can understand the context, sentiment, and deceptive tactics within a webpage's content, thereby mimicking the intuitive judgment of a human security expert and catching threats that automated rules would miss.

## Features

- **Heuristic Analysis**: Checks for suspicious URL patterns, IP addresses as hostnames, and new domain registrations.
- **AI Content Analysis**: Leverages Google's Gemini Pro to analyze webpage text for signs of phishing like urgency, impersonation, and grammatical errors.
- **Weighted Scoring**: Combines heuristic and AI scores for a comprehensive final verdict.
- **API-Ready**: Built with a Flask backend to be easily integrated into other applications or browser extensions.

## Technology Stack

- **Language**: Python 3.x
- **Core Libraries**: Flask, Requests, BeautifulSoup4, python-whois
- **AI Engine**: Google Gemini API
- **Frontend**: Browser Extension (HTML, CSS, JavaScript)

## Setup & Usage

To run this project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/phishguard-ai.git](https://github.com/YOUR_USERNAME/phishguard-ai.git)
    cd phishguard-ai
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *(You will need to create a `requirements.txt` file by running `pip freeze > requirements.txt`)*

3.  **Set your API Key:**
    Set your Gemini API key as an environment variable.
    ```bash
    # On macOS/Linux
    export GEMINI_API_KEY="YOUR_API_KEY_HERE"

    # On Windows
    set GEMINI_API_KEY="YOUR_API_KEY_HERE"
    ```

4.  **Run the Flask Server:**
    ```bash
    python app.py
    ```
    The server will be running at `http://127.0.0.1:5000`.

5.  **Load the Browser Extension:**
    - Open your browser and navigate to `chrome://extensions`.
    - Enable "Developer mode".
    - Click "Load unpacked" and select the browser extension folder.