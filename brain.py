import os
import json
import google.generativeai as genai

# --- Part 1: The AI Prompt Template (Updated for Accuracy) ---
# This new prompt is more strict to prevent hallucinations.
AI_PROMPT_TEMPLATE = """
You are PhishGuard AI, a highly factual cybersecurity analyst. Your task is to analyze ONLY the text provided below to determine if it's a phishing attempt.

**CRITICAL INSTRUCTIONS:**
1.  **Think step-by-step.** First, analyze the text for any of the specific red flags listed below.
2.  **If NO concrete red flags are found in the text, you MUST assign an "ai_score" of 0 or 1** and your justification must state that no suspicious indicators were found. This is the default action.
3.  **Only if you find clear, undeniable evidence** of a red flag should you assign a higher score.
4.  Your justification **must** quote the specific words or phrases from the text that you consider to be a red flag. Do not invent scenarios or assume the presence of elements (like pop-ups or update notices) that are not explicitly in the text.

**Red Flags to look for:**
- **Urgency/Threats:** Phrases like "account will be suspended," "immediate action required."
- **Generic Greetings:** "Dear Valued Customer."
- **Obvious Errors:** Clear spelling or grammar mistakes.
- **Credential Requests:** Direct requests for passwords, credit card info, etc.
- **Impersonation:** Language that feels like a clumsy attempt to copy a major brand (e.g., "Microsofts Support").

Based on your step-by-step analysis, you MUST return a JSON object with exactly two keys:
- "ai_score": An integer from 0 (Safe) to 10 (High-Risk Phishing).
- "justification": A brief explanation for your score. If no flags are found, state that clearly.

Here is the webpage text to analyze:
---
{webpage_text}
---
"""

def analyze_content_with_ai(webpage_text: str, api_key: str) -> dict:
    """
    Sends webpage text to the Gemini AI for phishing analysis.

    Args:
        webpage_text: The text content scraped from the website.
        api_key: Your Google AI Studio API key.

    Returns:
        A dictionary containing the 'ai_score', 'justification', and 'error' status.
    """
    # --- Part 2: Configuration and Input Validation ---
    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        return {"ai_score": -1, "justification": "", "error": f"API Configuration Failed: {e}"}

    model = genai.GenerativeModel("gemini-2.5-pro")

    if not webpage_text or webpage_text.isspace():
        return {"ai_score": 0, "justification": "Webpage was empty, no analysis performed.", "error": "Empty input text."}

    # --- Part 3: Sending the Request to the AI ---
    prompt = AI_PROMPT_TEMPLATE.format(webpage_text=webpage_text[:10000])

    try:
        response = model.generate_content(prompt)

        # --- Part 4: Parsing and Cleaning the AI's Response ---
        response_text = response.text.strip().replace("```json", "").replace("```", "").strip()
        result = json.loads(response_text)

        # --- Part 5: Validating the Parsed Data ---
        ai_score = result.get("ai_score")
        justification = result.get("justification")

        if isinstance(ai_score, int) and isinstance(justification, str):
            # The 'verdict' logic is best handled in your main application
            # after all scores are aggregated.
            return {"ai_score": ai_score, "justification": justification, "error": None}
        else:
            return {"ai_score": -1, "justification": "AI response had invalid data types.", "error": "Invalid data types in AI response."}

    # --- Part 6: Error Handling ---
    except json.JSONDecodeError:
        return {"ai_score": -1, "justification": "Failed to parse JSON from AI.", "error": f"Failed to parse JSON from AI response: {response.text}"}
    except Exception as e:
        return {"ai_score": -1, "justification": "An unexpected AI error occurred.", "error": f"An unexpected AI error occurred: {e}"}

# --- Main execution block for testing the function ---
if __name__ == "__main__":
    # IMPORTANT: Replace "YOUR_API_KEY_HERE" with your actual Gemini API key.
    my_api_key = "YOUR_API_KEY_HERE"

    if my_api_key == "YOUR_API_KEY_HERE":
        print("Please replace 'YOUR_API_KEY_HERE' with your actual API key.")
    else:
        # This is an example of a safe text from a known site.
        safe_text_example = """
            Home Trending Shorts Subscriptions Library History Your videos
            Watch later Liked videos Music Gaming Sports
            """
        
        print("\n--- Analyzing Safe Text (YouTube) ---")
        ai_report_safe = analyze_content_with_ai(safe_text_example, my_api_key)
        print(ai_report_safe)
