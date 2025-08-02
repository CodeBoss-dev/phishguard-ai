# PhishGuard AI 🛡️

A multi-vector phishing analysis engine using heuristics and generative AI. This tool analyzes URLs for phishing threats by combining rule-based checks with AI-driven content analysis.

### Core Components
- **scanner.py**: Fetches and parses webpage content.
- **heuristic.py**: Analyzes the URL for suspicious patterns.
- **brain.py**: Uses the Google Gemini API to analyze text for phishing indicators.
- **app.py**: A Flask server that exposes the analysis logic as an API.
- **Browser Extension**: A simple frontend to interact with the API.
