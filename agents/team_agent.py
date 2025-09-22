import json
from vertexai.generative_models import GenerativeModel
from utils.retry_handler import gemini_request_with_retry

def analyze_team(text_content: str) -> dict:
    """
    Analyzes team data from the text using a generative AI model.
    """
    print("Running Team Agent with Vertex AI...")

    model = GenerativeModel("gemini-1.5-flash")

    prompt = f"""
    Analyze the following startup description and extract details about the team.
    Return the result as a JSON object with the keys "founders_background", "team_size", and "ip_patents".
    For "founders_background", provide a brief summary of their experience. For "ip_patents", summarize any mention of intellectual property.
    If a metric is not found, set its value to "Not found".

    Text:
    ---
    {text_content}
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
            "founders_background": "Error",
            "team_size": "Error",
            "ip_patents": "Error"
        }
