import json
from vertexai.generative_models import GenerativeModel
from utils.retry_handler import gemini_request_with_retry

def analyze_public_data(company_name: str) -> dict:
    """
    Analyzes public data for the company using a generative AI model.
    """
    print("Running Public Data Agent with Vertex AI...")

    model = GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Based on your general knowledge, provide a summary of the public sentiment and any recent significant news for a company named '{company_name}'.

    Return the result as a JSON object with the keys "news_sentiment" (e.g., Positive, Negative, Neutral) and "public_data_summary".

    If the company is unknown or there is no significant public data, indicate that in the summary.

    JSON Output:
    """

    response = gemini_request_with_retry(model, prompt)

    try:
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing AI response: {e}")
        return {
            "news_sentiment": "Error",
            "public_data_summary": "Error processing public data analysis."
        }
