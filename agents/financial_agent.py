import json
from vertexai.generative_models import GenerativeModel
from utils.retry_handler import gemini_request_with_retry

def analyze_financials(text_content: str) -> dict:
    """
    Analyzes financial data from the text using a generative AI model.
    """
    print("Running Financial Agent with Vertex AI...")

    model = GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    You are a precise data extraction bot. Your task is to analyze the following text and extract specific financial metrics.

    Instructions:
    1.  Carefully read the text to find the following metrics: "revenue", "cac" (Customer Acquisition Cost), and "ltv" (Lifetime Value).
    2.  For "revenue", look for explicit mentions of 'revenue', 'ARR', 'Annual Recurring Revenue', or 'booked revenue'.
    3.  **CRITICAL:** Do not estimate, calculate, or assume any values. If a metric is not explicitly stated in the text, you MUST return "Not found" for that metric. Do not make up numbers.
    4.  Return the result as a single JSON object with the keys "revenue", "cac", and "ltv".

    Text:
    ---
    {text_content}
    ---

    JSON Output:
    """

    response = gemini_request_with_retry(model, prompt)

    try:
        # The response text might be enclosed in markdown backticks for JSON
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing AI response: {e}")
        return {
            "revenue": "Error",
            "cac": "Error",
            "ltv": "Error"
        }
