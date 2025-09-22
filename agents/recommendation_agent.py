import json
from vertexai.generative_models import GenerativeModel
from utils.retry_handler import gemini_request_with_retry

def generate_recommendation(final_data: dict) -> dict:
    """
    Generates a final investment recommendation based on all analyzed data.
    """
    print("Running Recommendation Agent with Vertex AI...")

    model = GenerativeModel("gemini-1.5-flash")

    input_data_str = json.dumps(final_data, indent=2)

    prompt = f"""
    You are a principal investment analyst at a venture capital firm. You have been provided with a structured JSON object containing comprehensive analysis of a startup, compiled from various specialist agents (financial, market, team, risk, benchmark, public data).

    Your task is to synthesize all of this information and provide a final investment recommendation.

    Based on the data, provide:
    1.  A "recommendation": one of BUY, HOLD, or PASS.
    2.  A "confidence" score (0-100) representing your conviction in the recommendation.
    3.  A concise "investment_rationale" (2-3 sentences) explaining the key factors that led to your decision, referencing the provided data (e.g., strong LTV/CAC, but high market risk).

    Return the result as a single JSON object with these three keys.

    Input Data:
    ---
    {input_data_str}
    ---

    JSON Output:
    """

    response = gemini_request_with_retry(model, prompt)

    try:
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error parsing AI response: {e}")
        return {
            "recommendation": "Error",
            "confidence": 0,
            "investment_rationale": "Error processing final recommendation."
        }
