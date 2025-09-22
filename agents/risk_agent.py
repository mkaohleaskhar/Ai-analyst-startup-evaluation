import json
from vertexai.generative_models import GenerativeModel
from utils.retry_handler import gemini_request_with_retry

def analyze_risk(analysis_data: dict) -> dict:
    """
    Analyzes risk based on data from other agents using a generative AI model.
    """
    print("Running Risk Agent with Vertex AI...")

    model = GenerativeModel("gemini-1.5-flash")

    # Convert the input data dictionary to a JSON string for the prompt
    input_data_str = json.dumps(analysis_data, indent=2)

    prompt = f"""
    As a startup risk analyst, review the following structured data which contains the output from financial, market, and team analysis agents.
    Identify potential risks in the startup.

    Based on the data, provide a brief summary for "financial_risk", "market_risk", and "execution_risk".
    Finally, provide an "overall_risk" level (LOW, MEDIUM, or HIGH).

    Return the result as a JSON object with the keys "financial_risk", "market_risk", "execution_risk", and "overall_risk".

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
            "financial_risk": "Error",
            "market_risk": "Error",
            "execution_risk": "Error",
            "overall_risk": "Error"
        }
